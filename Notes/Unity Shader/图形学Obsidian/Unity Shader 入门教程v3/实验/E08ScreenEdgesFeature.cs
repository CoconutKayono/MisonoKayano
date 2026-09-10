using UnityEngine;
using UnityEngine.Experimental.Rendering;
using UnityEngine.Rendering;
using UnityEngine.Rendering.RendererUtils;
using UnityEngine.Rendering.RenderGraphModule;
using UnityEngine.Rendering.Universal;

public class E08ScreenEdgesFeature : ScriptableRendererFeature
{
    public LayerMask groupA, groupB;
    public Material idMaterialA, idMaterialB, edgeMaterial;
    EdgePass pass;
    public override void Create()
    {
        pass = new EdgePass { renderPassEvent = RenderPassEvent.BeforeRenderingPostProcessing };
    }
    public override void AddRenderPasses(ScriptableRenderer renderer,ref RenderingData data)
    {
        if(idMaterialA==null || idMaterialB==null || edgeMaterial==null) return;
        if(!idMaterialA.shader.isSupported || !idMaterialB.shader.isSupported || !edgeMaterial.shader.isSupported) return;
        if(data.cameraData.cameraType!=CameraType.Game || data.cameraData.renderType!=CameraRenderType.Base) return;
        pass.a=groupA.value; pass.b=groupB.value;
        pass.matA=idMaterialA; pass.matB=idMaterialB; pass.effect=edgeMaterial;
        pass.ConfigureInput(ScriptableRenderPassInput.Depth | ScriptableRenderPassInput.Normal);
        renderer.EnqueuePass(pass);
    }
    class EdgePass : ScriptableRenderPass
    {
        public int a,b;
        public Material matA,matB,effect;
        static readonly int IdTexture = Shader.PropertyToID("_E08IdTexture");
        class IdData { public RendererListHandle a,b; }
        class EdgeData { public TextureHandle color; public Material material; }
        static RendererListHandle CreateList(RenderGraph graph,UniversalRenderingData rendering,
            UniversalCameraData camera,int layers,Material material)
        {
            var tags=new[] {new ShaderTagId("UniversalForward"),new ShaderTagId("UniversalForwardOnly"),
                            new ShaderTagId("SRPDefaultUnlit")};
            var desc=new RendererListDesc(tags,rendering.cullResults,camera.camera)
            {
                renderQueueRange=RenderQueueRange.opaque,
                sortingCriteria=SortingCriteria.CommonOpaque,
                layerMask=layers,
                overrideMaterial=material,
                overrideMaterialPassIndex=0
            };
            return graph.CreateRendererList(desc);
        }
        public override void RecordRenderGraph(RenderGraph graph,ContextContainer frameData)
        {
            var resources=frameData.Get<UniversalResourceData>();
            var rendering=frameData.Get<UniversalRenderingData>();
            var camera=frameData.Get<UniversalCameraData>();
            if(resources.isActiveTargetBackBuffer || !resources.activeDepthTexture.IsValid() ||
               !resources.cameraDepthTexture.IsValid() || !resources.cameraNormalsTexture.IsValid()) return;
            var source=resources.activeColorTexture;
            var desc=graph.GetTextureDesc(source);
            desc.depthBufferBits=DepthBits.None;
            desc.msaaSamples=MSAASamples.None;
            desc.bindTextureMS=false;
            desc.clearBuffer=false;
            desc.name="E08 Edge Color";
            var output=graph.CreateTexture(desc);
            desc.format=GraphicsFormat.R8G8B8A8_UNorm;
            desc.name="E08 Group IDs";
            var ids=graph.CreateTexture(desc);
            using(var builder=graph.AddRasterRenderPass<IdData>("E08 Visible Group IDs",out var data))
            {
                data.a=CreateList(graph,rendering,camera,a,matA);
                data.b=CreateList(graph,rendering,camera,b,matB);
                builder.UseRendererList(data.a);
                builder.UseRendererList(data.b);
                builder.SetRenderAttachment(ids,0,AccessFlags.WriteAll);
                builder.SetRenderAttachmentDepth(resources.activeDepthTexture,AccessFlags.Read);
                builder.SetGlobalTextureAfterPass(ids,IdTexture);
                builder.AllowPassCulling(false);
                builder.SetRenderFunc(static (IdData p,RasterGraphContext ctx)=>
                {
                    ctx.cmd.ClearRenderTarget(false,true,Color.clear);
                    ctx.cmd.DrawRendererList(p.a);
                    ctx.cmd.DrawRendererList(p.b);
                });
            }
            using(var builder=graph.AddRasterRenderPass<EdgeData>("E08 Screen Edges",out var data))
            {
                data.color=source; data.material=effect;
                builder.UseTexture(source,AccessFlags.Read);
                builder.UseTexture(resources.cameraDepthTexture,AccessFlags.Read);
                builder.UseTexture(resources.cameraNormalsTexture,AccessFlags.Read);
                builder.UseGlobalTexture(IdTexture,AccessFlags.Read);
                builder.SetRenderAttachment(output,0,AccessFlags.WriteAll);
                builder.SetRenderFunc(static (EdgeData p,RasterGraphContext ctx)=>
                    Blitter.BlitTexture(ctx.cmd,p.color,new Vector4(1,1,0,0),p.material,0));
            }
            resources.cameraColor=output;
        }
    }
}
