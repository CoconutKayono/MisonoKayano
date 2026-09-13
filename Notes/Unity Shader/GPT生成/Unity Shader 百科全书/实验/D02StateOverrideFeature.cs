using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.RendererUtils;
using UnityEngine.Rendering.RenderGraphModule;
using UnityEngine.Rendering.Universal;

public class D02StateOverrideFeature : ScriptableRendererFeature
{
    public LayerMask layers=~0;
    public bool overrideDepth=true;
    public bool includeDepthInMask=true;
    InspectPass pass;
    public override void Create()
    {
        pass=new InspectPass { renderPassEvent=RenderPassEvent.AfterRenderingOpaques };
    }
    public override void AddRenderPasses(ScriptableRenderer renderer,ref RenderingData data)
    {
        if(data.cameraData.cameraType!=CameraType.Game || data.cameraData.renderType!=CameraRenderType.Base) return;
        pass.layers=layers.value;
        pass.overrideDepth=overrideDepth;
        pass.includeDepthInMask=includeDepthInMask;
        renderer.EnqueuePass(pass);
    }
    class InspectPass : ScriptableRenderPass
    {
        public int layers;
        public bool overrideDepth, includeDepthInMask;
        class PassData { public RendererListHandle list; }
        public override void RecordRenderGraph(RenderGraph graph,ContextContainer frameData)
        {
            var rendering=frameData.Get<UniversalRenderingData>();
            var camera=frameData.Get<UniversalCameraData>();
            var resources=frameData.Get<UniversalResourceData>();
            var desc=new RendererListDesc(new ShaderTagId("D02Inspect"),rendering.cullResults,camera.camera)
            {
                renderQueueRange=RenderQueueRange.opaque,
                sortingCriteria=camera.defaultOpaqueSortFlags,
                layerMask=layers
            };
            if(overrideDepth)
            {
                var state=new RenderStateBlock(includeDepthInMask ? RenderStateMask.Depth : RenderStateMask.Nothing);
                state.depthState=new DepthState(false,CompareFunction.Always);
                desc.stateBlock=state;
            }
            using(var builder=graph.AddRasterRenderPass<PassData>("D02 State Override",out var data))
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
