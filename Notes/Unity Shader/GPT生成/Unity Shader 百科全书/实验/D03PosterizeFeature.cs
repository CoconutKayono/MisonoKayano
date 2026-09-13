using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.RenderGraphModule;
using UnityEngine.Rendering.Universal;

public class D03PosterizeFeature : ScriptableRendererFeature
{
    public Material effectMaterial;
    public bool traceNextFrame;
    PosterizePass pass;
    public override void Create()
    {
        pass=new PosterizePass { renderPassEvent=RenderPassEvent.BeforeRenderingPostProcessing };
    }
    public override void AddRenderPasses(ScriptableRenderer renderer,ref RenderingData data)
    {
        if(effectMaterial==null || !effectMaterial.shader.isSupported) return;
        if(data.cameraData.cameraType!=CameraType.Game || data.cameraData.renderType!=CameraRenderType.Base) return;
        pass.material=effectMaterial;
        pass.trace=traceNextFrame;
        traceNextFrame=false;
        renderer.EnqueuePass(pass);
    }
    class PosterizePass : ScriptableRenderPass
    {
        public Material material;
        public bool trace;
        class PassData
        {
            public TextureHandle source;
            public Material material;
            public bool trace;
        }
        public override void RecordRenderGraph(RenderGraph graph,ContextContainer frameData)
        {
            var resources=frameData.Get<UniversalResourceData>();
            if(resources.isActiveTargetBackBuffer)
            {
                if(trace) Debug.LogWarning("D03 skipped: use an intermediate camera color texture.");
                return;
            }
            TextureHandle source=resources.activeColorTexture;
            var desc=graph.GetTextureDesc(source);
            desc.name="D03 Posterized Color";
            desc.depthBufferBits=DepthBits.None;
            desc.msaaSamples=MSAASamples.None;
            desc.bindTextureMS=false;
            desc.clearBuffer=false;
            TextureHandle destination=graph.CreateTexture(desc);
            if(trace) Debug.Log("D03: CPU is recording the graph.");
            using(var builder=graph.AddRasterRenderPass<PassData>("D03 Posterize",out var data))
            {
                data.source=source;
                data.material=material;
                data.trace=trace;
                builder.UseTexture(source,AccessFlags.Read);
                builder.SetRenderAttachment(destination,0,AccessFlags.WriteAll);
                builder.SetRenderFunc(static (PassData p,RasterGraphContext ctx)=>
                {
                    if(p.trace) Debug.Log("D03: CPU callback is recording a blit, not waiting for GPU completion.");
                    Blitter.BlitTexture(ctx.cmd,p.source,new Vector4(1,1,0,0),p.material,0);
                });
            }
            resources.cameraColor=destination;
        }
    }
}
