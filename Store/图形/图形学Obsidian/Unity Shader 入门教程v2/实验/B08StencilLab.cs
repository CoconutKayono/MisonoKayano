using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Experimental.Rendering;

public class B08StencilLab : MonoBehaviour
{
    public Material labMaterial;
    [Range(0,255)] public int initialStencil=0;
    public bool readerFirst=false;
    RenderTexture target;
    Mesh quad;
    CommandBuffer commands;
    bool ready;
    void Start()
    {
        if(labMaterial==null || !labMaterial.shader.isSupported) return;
        var descriptor=new RenderTextureDescriptor(128,128);
        descriptor.graphicsFormat=GraphicsFormat.R8G8B8A8_UNorm;
        descriptor.depthStencilFormat=GraphicsFormat.D24_UNorm_S8_UInt;
        descriptor.msaaSamples=1;
        target=new RenderTexture(descriptor) { name="B08 Owned Depth Stencil" };
        if(!target.Create()) { Debug.LogError("RenderTexture creation failed."); return; }
        var actual=target.depthStencilFormat;
        if(actual!=GraphicsFormat.D24_UNorm_S8_UInt &&
           actual!=GraphicsFormat.D32_SFloat_S8_UInt)
        {
            Debug.LogError("This lab requires a verified stencil format: "+actual);
            return;
        }
        quad=new Mesh { name="B08 Owned Quad" };
        quad.vertices=new Vector3[] {
            new Vector3(-1,-1,0),new Vector3(1,-1,0),
            new Vector3(1,1,0),new Vector3(-1,1,0) };
        quad.triangles=new int[] {0,1,2,0,2,3};
        commands=new CommandBuffer { name="B08 Stencil Writer Reader" };
        ready=true;
        Debug.Log("Actual depth/stencil format: "+actual);
    }
    void Update()
    {
        if(!ready || labMaterial==null) return;
        commands.Clear();
        commands.SetRenderTarget(target);
        commands.SetViewport(new Rect(0,0,128,128));
        commands.ClearRenderTarget(true,true,Color.black,1f,(uint)initialStencil);
        commands.DrawMesh(quad,Matrix4x4.identity,labMaterial,0,readerFirst ? 1 : 0);
        commands.DrawMesh(quad,Matrix4x4.identity,labMaterial,0,readerFirst ? 0 : 1);
        Graphics.ExecuteCommandBuffer(commands);
    }
    void OnGUI()
    {
        if(ready) GUI.DrawTexture(new Rect(10,10,256,256),target,ScaleMode.ScaleToFit,false);
    }
    void OnDestroy()
    {
        if(commands!=null) commands.Release();
        if(target!=null) { target.Release(); Destroy(target); }
        if(quad!=null) Destroy(quad);
    }
}
