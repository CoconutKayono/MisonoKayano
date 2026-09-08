using UnityEngine;
using UnityEngine.Rendering;

public class C07SkinningLab : MonoBehaviour
{
    public Shader labShader;
    [Range(0,0.5f)] public float amplitude=0.2f;
    public bool matchDepthAndShadow=true;
    GameObject ownedRoot;
    Transform upper;
    SkinnedMeshRenderer skin;
    Mesh inputMesh, snapshot;
    Material liveMaterial, snapshotMaterial;
    bool ready;
    void Start()
    {
        if(labShader==null || !labShader.isSupported) return;
        ownedRoot=new GameObject("C07 Owned Experiment");
        ownedRoot.transform.SetParent(transform,false);
        var live=new GameObject("Live Skinned Strip");
        live.transform.SetParent(ownedRoot.transform,false);
        var lower=new GameObject("Lower Bone").transform;
        lower.SetParent(live.transform,false);
        upper=new GameObject("Upper Bone").transform;
        upper.SetParent(lower,false);
        upper.localPosition=Vector3.up;
        inputMesh=new Mesh { name="C07 Two Bone Strip" };
        const int segments=16;
        var positions=new Vector3[(segments+1)*2];
        var normals=new Vector3[positions.Length];
        var weights=new BoneWeight[positions.Length];
        var triangles=new int[segments*6];
        for(int row=0;row<=segments;row++)
        {
            float y=2f*row/segments;
            float w=Mathf.Clamp01(y-0.5f);
            for(int col=0;col<2;col++)
            {
                int i=row*2+col;
                positions[i]=new Vector3(col==0 ? -0.25f : 0.25f,y,0);
                normals[i]=Vector3.back;
                weights[i]=new BoneWeight { boneIndex0=0,weight0=1-w,boneIndex1=1,weight1=w };
            }
            if(row<segments)
            {
                int i=row*2, t=row*6;
                triangles[t]=i; triangles[t+1]=i+2; triangles[t+2]=i+1;
                triangles[t+3]=i+1; triangles[t+4]=i+2; triangles[t+5]=i+3;
            }
        }
        inputMesh.vertices=positions; inputMesh.normals=normals;
        inputMesh.triangles=triangles; inputMesh.boneWeights=weights;
        inputMesh.bindposes=new Matrix4x4[] {
            lower.worldToLocalMatrix*live.transform.localToWorldMatrix,
            upper.worldToLocalMatrix*live.transform.localToWorldMatrix };
        liveMaterial=new Material(labShader);
        skin=live.AddComponent<SkinnedMeshRenderer>();
        skin.sharedMesh=inputMesh;
        skin.bones=new Transform[] {lower,upper}; skin.rootBone=lower;
        skin.quality=SkinQuality.Bone2;
        skin.sharedMaterial=liveMaterial;
        skin.updateWhenOffscreen=false;
        skin.localBounds=new Bounds(new Vector3(0,1,0),new Vector3(4,4,2));
        var frozen=new GameObject("CPU Snapshot Without Shader Displacement");
        frozen.transform.SetParent(ownedRoot.transform,false);
        frozen.transform.localPosition=new Vector3(1.8f,0,0);
        snapshot=new Mesh { name="C07 CPU Snapshot" };
        frozen.AddComponent<MeshFilter>().sharedMesh=snapshot;
        snapshotMaterial=new Material(labShader);
        snapshotMaterial.SetFloat("_Amplitude",0);
        snapshotMaterial.SetColor("_Color",new Color(1,0.6f,0.1f,1));
        frozen.AddComponent<MeshRenderer>().sharedMaterial=snapshotMaterial;
        ready=true;
        UpdatePose();
        BakeSnapshot();
    }
    void UpdatePose()
    {
        upper.localRotation=Quaternion.AngleAxis(35*Mathf.Sin(Time.time),Vector3.forward);
        liveMaterial.SetFloat("_Amplitude",amplitude);
        liveMaterial.SetFloat("_MatchAux",matchDepthAndShadow ? 1 : 0);
    }
    void LateUpdate() { if(ready) UpdatePose(); }
    [ContextMenu("Bake Snapshot")]
    public void BakeSnapshot()
    {
        if(!ready) return;
        UpdatePose();
        skin.BakeMesh(snapshot,false);
        snapshot.RecalculateBounds();
    }
    void OnGUI()
    {
        if(ready && GUI.Button(new Rect(10,10,180,30),"Bake Snapshot")) BakeSnapshot();
    }
    void OnDestroy()
    {
        if(ownedRoot!=null) Destroy(ownedRoot);
        if(inputMesh!=null) Destroy(inputMesh);
        if(snapshot!=null) Destroy(snapshot);
        if(liveMaterial!=null) Destroy(liveMaterial);
        if(snapshotMaterial!=null) Destroy(snapshotMaterial);
    }
}
