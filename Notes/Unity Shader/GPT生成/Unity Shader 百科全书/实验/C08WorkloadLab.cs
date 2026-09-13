using UnityEngine;
using UnityEngine.Rendering;

public class C08WorkloadLab : MonoBehaviour
{
    public enum Layout { Layered, Partitioned }
    public Shader labShader;
    public Layout layout;
    [Range(64,2048)] public int resolution=512;
    [Range(1,64)] public int layers=8;
    [Range(1,16)] public int gridSide=4;
    [Range(0,128)] public int iterations=16;
    public bool showPreview=true;
    Material material;
    Mesh quad;
    RenderTexture target;
    CommandBuffer commands;
    string status;
    bool ready;
    void Start()
    {
        if(labShader==null || !labShader.isSupported) return;
        material=new Material(labShader);
        quad=new Mesh { name="C08 Owned Quad" };
        quad.vertices=new Vector3[] {
            new Vector3(-1,-1,0),new Vector3(1,-1,0),
            new Vector3(1,1,0),new Vector3(-1,1,0) };
        quad.triangles=new int[] {0,1,2,0,2,3};
        commands=new CommandBuffer { name="C08 Replayed Workload" };
        RebuildWorkload();
    }
    [ContextMenu("Rebuild Workload")]
    public void RebuildWorkload()
    {
        if(!Application.isPlaying || material==null) return;
        ready=false;
        commands.Clear();
        if(target!=null) { target.Release(); Destroy(target); }
        int size=Mathf.Clamp(resolution,64,2048);
        int n=Mathf.Clamp(gridSide,1,16), count=Mathf.Clamp(layers,1,64);
        target=new RenderTexture(size,size,0,RenderTextureFormat.ARGBHalf,RenderTextureReadWrite.Linear);
        target.name="C08 Workload Color";
        target.filterMode=FilterMode.Point;
        if(!target.Create()) { Debug.LogError("C08 target creation failed."); return; }
        var properties=new MaterialPropertyBlock();
        properties.SetInt("_Iterations",Mathf.Clamp(iterations,0,128));
        properties.SetFloat("_Contribution",layout==Layout.Layered ? 1f/count : 1f);
        commands.SetRenderTarget(target);
        commands.SetViewport(new Rect(0,0,size,size));
        commands.ClearRenderTarget(false,true,Color.clear);
        commands.BeginSample("C08 Workload");
        if(layout==Layout.Layered)
        {
            for(int i=0;i<count;i++) commands.DrawMesh(quad,Matrix4x4.identity,material,0,0,properties);
        }
        else
        {
            count=n*n;
            for(int y=0;y<n;y++) for(int x=0;x<n;x++)
            {
                int x0=x*size/n, x1=(x+1)*size/n;
                int y0=y*size/n, y1=(y+1)*size/n;
                commands.SetViewport(new Rect(x0,y0,x1-x0,y1-y0));
                commands.DrawMesh(quad,Matrix4x4.identity,material,0,0,properties);
            }
        }
        commands.EndSample("C08 Workload");
        status=layout+" | "+size+" square | draws="+count+" | iterations="+Mathf.Clamp(iterations,0,128);
        ready=true;
        Debug.Log("C08 rebuilt: "+status);
    }
    void Update() { if(ready) Graphics.ExecuteCommandBuffer(commands); }
    void OnGUI()
    {
        if(!ready || !showPreview) return;
        GUI.Label(new Rect(10,10,750,25),status);
        GUI.DrawTexture(new Rect(10,40,512,512),target,ScaleMode.ScaleToFit,false);
    }
    void OnDestroy()
    {
        if(commands!=null) commands.Release();
        if(target!=null) { target.Release(); Destroy(target); }
        if(material!=null) Destroy(material);
        if(quad!=null) Destroy(quad);
    }
}
