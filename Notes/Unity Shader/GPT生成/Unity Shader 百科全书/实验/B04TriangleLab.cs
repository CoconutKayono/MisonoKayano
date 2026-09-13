using UnityEngine;

[RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]
public class B04TriangleLab : MonoBehaviour
{
    public bool reverseIndices;
    public bool reverseNormals;
    Mesh ownedMesh;
    Mesh previousMesh;
    MeshFilter filter;
    void Start()
    {
        filter=GetComponent<MeshFilter>();
        previousMesh=filter.sharedMesh;
        ownedMesh=new Mesh { name="B04 Owned Triangle" };
        filter.sharedMesh=ownedMesh;
        Rebuild();
    }
    [ContextMenu("Rebuild Triangle")]
    public void Rebuild()
    {
        if (!Application.isPlaying || ownedMesh==null)
        {
            Debug.LogWarning("Enter Play Mode before rebuilding.");
            return;
        }
        ownedMesh.Clear();
        ownedMesh.vertices=new Vector3[] {
            new Vector3(-0.7f,-0.6f,0),
            new Vector3(0,0.7f,0),
            new Vector3(0.7f,-0.6f,0) };
        Vector3 n=reverseNormals ? Vector3.back : Vector3.forward;
        ownedMesh.normals=new Vector3[] { n,n,n };
        ownedMesh.triangles=reverseIndices ? new int[] {0,2,1} : new int[] {0,1,2};
        // Shader uses clip-space positions; a generous bound keeps this lab visible.
        ownedMesh.bounds=new Bounds(Vector3.zero,Vector3.one*10000);
    }
    void OnDestroy()
    {
        if (filter!=null && filter.sharedMesh==ownedMesh)
            filter.sharedMesh=previousMesh;
        if (ownedMesh!=null) Destroy(ownedMesh);
    }
}
