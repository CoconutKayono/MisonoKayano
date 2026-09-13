using UnityEngine;
using UnityEngine.Experimental.Rendering;
using UnityEngine.Rendering;
using UnityEngine.Rendering.RenderGraphModule;
using UnityEngine.Rendering.Universal;

public class D04LifetimeFeature : ScriptableRendererFeature
{
    public enum Mode { InternalConsumed, InternalUnused, ImportedUnused, ImportedReadUnused }
    public Mode mode;
    public bool forceKeepProducer;
    LifetimePass pass;
    public override void Create()
    {
        pass?.Dispose();
        pass=new LifetimePass { renderPassEvent=RenderPassEvent.BeforeRenderingPostProcessing };
    }
    public override void AddRenderPasses(ScriptableRenderer renderer,ref RenderingData data)
    {
        if(data.cameraData.cameraType!=CameraType.Game || data.cameraData.renderType!=CameraRenderType.Base) return;
        pass.mode=mode;
        pass.forceKeep=forceKeepProducer;
        renderer.EnqueuePass(pass);
    }
    protected override void Dispose(bool disposing) { pass?.Dispose(); pass=null; }
    class LifetimePass : ScriptableRenderPass
    {
        public Mode mode;
        public bool forceKeep;
        RTHandle owned;
        class ClearData { public Color color; }
        class CopyData { public TextureHandle source; }
        public LifetimePass()
        {
            owned=RTHandles.Alloc(256,256,depthBufferBits:DepthBits.None,
                colorFormat:GraphicsFormat.R8G8B8A8_UNorm,
                filterMode:FilterMode.Point,wrapMode:TextureWrapMode.Clamp,
                name:"D04 Owned Persistent Texture");
        }
        public void Dispose() { owned?.Release(); owned=null; }
        static TextureHandle MakeInternal(RenderGraph graph,string name)
        {
            var desc=new TextureDesc(256,256)
            {
                name=name,
                format=GraphicsFormat.R8G8B8A8_UNorm,
                msaaSamples=MSAASamples.None,
                clearBuffer=false,
                filterMode=FilterMode.Point
            };
            return graph.CreateTexture(desc);
        }
        public override void RecordRenderGraph(RenderGraph graph,ContextContainer frameData)
        {
            var resources=frameData.Get<UniversalResourceData>();
            bool imported=mode==Mode.ImportedUnused || mode==Mode.ImportedReadUnused;
            TextureHandle produced=imported ? graph.ImportTexture(owned) : MakeInternal(graph,"D04 Internal Product");
            using(var builder=graph.AddRasterRenderPass<ClearData>("D04 Producer",out var data))
            {
                data.color=Color.magenta;
                builder.SetRenderAttachment(produced,0,AccessFlags.WriteAll);
                if(forceKeep) builder.AllowPassCulling(false);
                builder.SetRenderFunc(static (ClearData p,RasterGraphContext ctx)=>
                    ctx.cmd.ClearRenderTarget(false,true,p.color));
            }
            bool consume=mode==Mode.InternalConsumed || mode==Mode.ImportedReadUnused;
            if(!consume) return;
            TextureHandle destination=mode==Mode.InternalConsumed
                ? resources.activeColorTexture : MakeInternal(graph,"D04 Unused Copy");
            using(var builder=graph.AddRasterRenderPass<CopyData>("D04 Consumer",out var data))
            {
                data.source=produced;
                builder.UseTexture(produced,AccessFlags.Read);
                builder.SetRenderAttachment(destination,0,AccessFlags.WriteAll);
                builder.SetRenderFunc(static (CopyData p,RasterGraphContext ctx)=>
                    Blitter.BlitTexture(ctx.cmd,p.source,new Vector4(1,1,0,0),0,false));
            }
        }
    }
}
