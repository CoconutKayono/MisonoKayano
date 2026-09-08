using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Experimental.Rendering;

public class C05LoadStoreLab : MonoBehaviour
{
    public enum OldContent { Preserve, ClearBlack, Discard }
    public Shader labShader;
    public OldContent oldContent;
    RenderTexture target;
    Material material;
    Mesh quad;
    CommandBuffer first, second;
    MaterialPropertyBlock red, green;
    bool ready;
    void Start()
    {
        if(labShader==null || !labShader.isSupported) return;
        var d=new RenderTextureDescriptor(256,256);
        d.graphicsFormat=GraphicsFormat.R8G8B8A8_UNorm;
        d.depthStencilFormat=GraphicsFormat.None;
        d.msaaSamples=1;
        target=new RenderTexture(d) { name="C05 Color", filterMode=FilterMode.Point };
        if(!target.Create()) { Debug.LogError("C05 target creation failed."); return; }
        material=new Material(labShader);
        quad=new Mesh { name="C05 Owned Quad" };
        quad.vertices=new Vector3[] {
            new Vector3(-1,-1,0),new Vector3(1,-1,0),
            new Vector3(1,1,0),new Vector3(-1,1,0) };
        quad.triangles=new int[] {0,1,2,0,2,3};
        red=new MaterialPropertyBlock(); red.SetColor("_Color",Color.red);
        green=new MaterialPropertyBlock(); green.SetColor("_Color",Color.green);
        first=new CommandBuffer { name="C05 Full Red" };
        second=new CommandBuffer { name="C05 Partial Green" };
        ready=true;
    }
    void Update()
    {
        if(!ready) return;
        first.Clear();
        first.SetRenderTarget(target,RenderBufferLoadAction.DontCare,RenderBufferStoreAction.Store);
        first.SetViewport(new Rect(0,0,256,256));
        first.DrawMesh(quad,Matrix4x4.identity,material,0,0,red);
        Graphics.ExecuteCommandBuffer(first);

        second.Clear();
        var load=oldContent==OldContent.Preserve ? RenderBufferLoadAction.Load : RenderBufferLoadAction.DontCare;
        second.SetRenderTarget(target,load,RenderBufferStoreAction.Store);
        second.SetViewport(new Rect(0,0,256,256));
        if(oldContent==OldContent.ClearBlack) second.ClearRenderTarget(false,true,Color.black);
        second.SetViewport(new Rect(128,0,128,256));
        second.DrawMesh(quad,Matrix4x4.identity,material,0,0,green);
        Graphics.ExecuteCommandBuffer(second);
    }
    void OnGUI()
    {
        if(!ready) return;
        GUI.Label(new Rect(10,10,700,25),oldContent+" | Discard does not define the left half");
        GUI.DrawTexture(new Rect(10,40,512,512),target,ScaleMode.ScaleToFit,false);
    }
    void OnDestroy()
    {
        if(first!=null) first.Release();
        if(second!=null) second.Release();
        if(target!=null) { target.Release(); Destroy(target); }
        if(material!=null) Destroy(material);
        if(quad!=null) Destroy(quad);
    }
}
