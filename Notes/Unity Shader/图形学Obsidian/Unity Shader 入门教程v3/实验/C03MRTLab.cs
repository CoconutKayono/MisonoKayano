using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Experimental.Rendering;

public class C03MRTLab : MonoBehaviour
{
    public Material labMaterial;
    public bool swapBindings;
    RenderTexture beauty, id;
    Mesh quad;
    CommandBuffer commands;
    bool ready;

    void Start()
    {
        if(labMaterial==null || !labMaterial.shader.isSupported ||
           SystemInfo.supportedRenderTargetCount<2)
        {
            Debug.LogError("Assign the C03 material; device must support two MRTs.");
            return;
        }
        var d=new RenderTextureDescriptor(128,128);
        d.graphicsFormat=GraphicsFormat.R8G8B8A8_UNorm;
        d.depthStencilFormat=GraphicsFormat.D24_UNorm_S8_UInt;
        d.msaaSamples=1;
        beauty=new RenderTexture(d) { name="C03 Beauty", filterMode=FilterMode.Point };
        d.depthStencilFormat=GraphicsFormat.None;
        id=new RenderTexture(d) { name="C03 ID", filterMode=FilterMode.Point };
        if(!beauty.Create() || !id.Create() ||
           beauty.graphicsFormat!=GraphicsFormat.R8G8B8A8_UNorm ||
           id.graphicsFormat!=beauty.graphicsFormat ||
           beauty.depthStencilFormat==GraphicsFormat.None)
        {
            Debug.LogError("C03 attachment creation/format requirements failed.");
            return;
        }
        quad=new Mesh { name="C03 Owned Quad" };
        quad.vertices=new Vector3[] {
            new Vector3(-0.8f,-0.8f,0),new Vector3(0.8f,-0.8f,0),
            new Vector3(0.8f,0.8f,0),new Vector3(-0.8f,0.8f,0) };
        quad.uv=new Vector2[] { Vector2.zero,Vector2.right,Vector2.one,Vector2.up };
        quad.triangles=new int[] {0,1,2,0,2,3};
        commands=new CommandBuffer { name="C03 One Draw Two Attachments" };
        ready=true;
        Debug.Log("C03 actual depth format: "+beauty.depthStencilFormat);
    }

    void Update()
    {
        if(!ready || labMaterial==null) return;
        var colors=new RenderTargetIdentifier[] {
            swapBindings ? id : beauty, swapBindings ? beauty : id };
        commands.Clear();
        commands.SetRenderTarget(colors,new RenderTargetIdentifier(beauty));
        commands.SetViewport(new Rect(0,0,128,128));
        commands.ClearRenderTarget(true,true,Color.clear);
        commands.DrawMesh(quad,Matrix4x4.identity,labMaterial,0,0);
        Graphics.ExecuteCommandBuffer(commands);
    }

    void OnGUI()
    {
        if(!ready) return;
        GUI.Label(new Rect(10,10,256,25),"Beauty resource");
        GUI.Label(new Rect(280,10,256,25),"ID resource");
        GUI.DrawTexture(new Rect(10,40,256,256),beauty,ScaleMode.ScaleToFit,false);
        GUI.DrawTexture(new Rect(280,40,256,256),id,ScaleMode.ScaleToFit,false);
    }

    void OnDestroy()
    {
        if(commands!=null) commands.Release();
        if(beauty!=null) { beauty.Release(); Destroy(beauty); }
        if(id!=null) { id.Release(); Destroy(id); }
        if(quad!=null) Destroy(quad);
    }
}
