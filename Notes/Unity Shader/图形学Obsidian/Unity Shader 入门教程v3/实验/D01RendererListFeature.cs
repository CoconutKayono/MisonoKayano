using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.RendererUtils;
using UnityEngine.Rendering.RenderGraphModule;
using UnityEngine.Rendering.Universal;

public class D01RendererListFeature : ScriptableRendererFeature
{
    public LayerMask layers=~0;
    ListPass pass;
    public override void Create()
    {
        pass=new ListPass { renderPassEvent=RenderPassEvent.AfterRenderingOpaques };
    }
    public override void AddRenderPasses(ScriptableRenderer renderer,ref RenderingData data)
    {
        if(data.cameraData.cameraType!=CameraType.Game || data.cameraData.renderType!=CameraRenderType.Base) return;
        pass.layers=layers.value;
        renderer.EnqueuePass(pass);
    }
    class ListPass : ScriptableRenderPass
    {
        public int layers;
        class PassData { public RendererListHandle list; }
        public override void RecordRenderGraph(RenderGraph graph,ContextContainer frameData)
        {
            var rendering=frameData.Get<UniversalRenderingData>();
            var camera=frameData.Get<UniversalCameraData>();
            var resources=frameData.Get<UniversalResourceData>();
            var desc=new RendererListDesc(new ShaderTagId("D01Mask"),rendering.cullResults,camera.camera)
            {
                renderQueueRange=RenderQueueRange.opaque,
                sortingCriteria=camera.defaultOpaqueSortFlags,
                layerMask=layers
            };
            using(var builder=graph.AddRasterRenderPass<PassData>("D01 Filtered Objects",out var data))
            {
                data.list=graph.CreateRendererList(desc);
                builder.UseRendererList(data.list);
                builder.SetRenderAttachment(resources.activeColorTexture,0,AccessFlags.ReadWrite);
                builder.SetRenderAttachmentDepth(resources.activeDepthTexture,AccessFlags.Read);
                builder.SetRenderFunc(static (PassData p,RasterGraphContext ctx)=>ctx.cmd.DrawRendererList(p.list));
            }
        }
    }
}
