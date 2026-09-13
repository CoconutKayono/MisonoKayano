using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Experimental.Rendering;

public class C04MSAALab : MonoBehaviour
{
    public enum ViewMode { SolidAlphaIgnored, Clip, AlphaToCoverage, AlphaBlend }
    public Shader labShader;
    public ViewMode mode;
    [Tooltip("Use 1, 2, 4 or 8. In Play mode call Rebuild Targets after changing.")]
    public int requestedSamples=4;
    RenderTexture source, resolved;
    Material material;
    Texture2D mask;
    Mesh quad;
    CommandBuffer commands;
    int actualSamples;
    bool ready;

    void Start()
    {
        if(labShader==null || !labShader.isSupported)
        {
            Debug.LogError("Assign the supported C04 shader.");
            return;
        }
        material=new Material(labShader);
        mask=new Texture2D(128,128,TextureFormat.RGBA32,false,true);
        mask.name="C04 Owned Linear Alpha Mask";
        mask.wrapMode=TextureWrapMode.Clamp;
        mask.filterMode=FilterMode.Bilinear;
        var pixels=new Color32[128*128];
        for(int y=0;y<128;y++) for(int x=0;x<128;x++)
        {
            float u=(x+0.5f)/128-0.5f, v=(y+0.5f)/128-0.5f;
            float a=1-Mathf.InverseLerp(0.30f,0.38f,Mathf.Sqrt(u*u+v*v));
            pixels[y*128+x]=new Color32(255,255,255,(byte)Mathf.RoundToInt(a*255));
        }
        mask.SetPixels32(pixels);
        mask.Apply(false,true);
        material.SetTexture("_Mask",mask);
        quad=new Mesh { name="C04 Owned Tilted Quad" };
        quad.vertices=new Vector3[] {
            new Vector3(-0.85f,-0.65f,0),new Vector3(0.65f,-0.85f,0),
            new Vector3(0.85f,0.65f,0),new Vector3(-0.65f,0.85f,0) };
        quad.uv=new Vector2[] { Vector2.zero,Vector2.right,Vector2.one,Vector2.up };
        quad.triangles=new int[] {0,1,2,0,2,3};
        commands=new CommandBuffer { name="C04 Coverage And Explicit Resolve" };
        RebuildTargets();
    }

    [ContextMenu("Rebuild Targets")]
    public void RebuildTargets()
    {
        if(!Application.isPlaying || material==null) return;
        ready=false;
        commands.Clear();
        ReleaseTarget(ref source);
        ReleaseTarget(ref resolved);
        if(requestedSamples!=1 && requestedSamples!=2 &&
           requestedSamples!=4 && requestedSamples!=8)
        {
            Debug.LogError("Requested samples must be 1, 2, 4 or 8.");
            return;
        }
        var d=new RenderTextureDescriptor(256,256);
        d.graphicsFormat=GraphicsFormat.R8G8B8A8_UNorm;
        d.depthStencilFormat=GraphicsFormat.D24_UNorm_S8_UInt;
        d.msaaSamples=requestedSamples;
        d.msaaSamples=SystemInfo.GetRenderTextureSupportedMSAASampleCount(d);
        if(d.msaaSamples<1) { Debug.LogError("No supported sample count."); return; }
        d.bindMS=d.msaaSamples>1;
        source=new RenderTexture(d) { name="C04 MSAA Source" };
        if(!source.Create() || source.graphicsFormat!=GraphicsFormat.R8G8B8A8_UNorm ||
           source.depthStencilFormat==GraphicsFormat.None)
        {
            Debug.LogError("C04 source creation/format failed.");
            return;
        }
        actualSamples=source.antiAliasing;
        d.graphicsFormat=source.graphicsFormat;
        d.depthStencilFormat=GraphicsFormat.None;
        d.msaaSamples=1;
        d.bindMS=false;
        resolved=new RenderTexture(d) { name="C04 Resolved", filterMode=FilterMode.Point };
        if(!resolved.Create() || resolved.graphicsFormat!=source.graphicsFormat)
        {
            Debug.LogError("C04 resolve target creation/format failed.");
            return;
        }
        ready=true;
        Debug.Log("C04 requested/actual samples: "+requestedSamples+"/"+actualSamples);
    }

    void Update()
    {
        if(!ready) return;
        commands.Clear();
        commands.SetRenderTarget(source);
        commands.SetViewport(new Rect(0,0,256,256));
        commands.ClearRenderTarget(true,true,Color.black);
        if(mode!=ViewMode.AlphaToCoverage || actualSamples>1)
            commands.DrawMesh(quad,Matrix4x4.identity,material,0,(int)mode);
        if(actualSamples>1) commands.ResolveAntiAliasedSurface(source,resolved);
        else commands.Blit(source,resolved);
        Graphics.ExecuteCommandBuffer(commands);
    }

    void OnGUI()
    {
        if(!ready) return;
        string status=mode+" | requested/actual: "+requestedSamples+"/"+actualSamples;
        if(mode==ViewMode.AlphaToCoverage && actualSamples==1)
            status+=" | A2C skipped: MSAA required";
        GUI.Label(new Rect(10,10,760,25),status);
        GUI.DrawTexture(new Rect(10,40,512,512),resolved,ScaleMode.ScaleToFit,false);
    }

    void ReleaseTarget(ref RenderTexture target)
    {
        if(target==null) return;
        target.Release();
        Destroy(target);
        target=null;
    }

    void OnDestroy()
    {
        if(commands!=null) commands.Release();
        ReleaseTarget(ref source);
        ReleaseTarget(ref resolved);
        if(material!=null) Destroy(material);
        if(mask!=null) Destroy(mask);
        if(quad!=null) Destroy(quad);
    }
}
