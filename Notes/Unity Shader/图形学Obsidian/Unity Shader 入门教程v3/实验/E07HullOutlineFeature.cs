using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.RendererUtils;
using UnityEngine.Rendering.RenderGraphModule;
using UnityEngine.Rendering.Universal;

public class E07HullOutlineFeature : ScriptableRendererFeature
{
    public LayerMask layers;
    public Material outlineMaterial;
    HullPass pass;
    public override void Create()
    {
        pass = new HullPass { renderPassEvent = RenderPassEvent.BeforeRenderingPostProcessing };
    }
    public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData data)
    {
        if (outlineMaterial == null || !outlineMaterial.shader.isSupported || layers.value == 0) return;
        if (data.cameraData.cameraType != CameraType.Game || data.cameraData.renderType != CameraRenderType.Base) return;
        pass.material = outlineMaterial;
        pass.layers = layers.value;
        renderer.EnqueuePass(pass);
    }
    class HullPass : ScriptableRenderPass
    {
        public Material material;
        public int layers;
        class PassData { public RendererListHandle list; }
        public override void RecordRenderGraph(RenderGraph graph, ContextContainer frameData)
        {
            var rendering = frameData.Get<UniversalRenderingData>();
            var camera = frameData.Get<UniversalCameraData>();
            var resources = frameData.Get<UniversalResourceData>();
            if (!resources.activeDepthTexture.IsValid()) return;
            var tags = new[] { new ShaderTagId("UniversalForward"), new ShaderTagId("UniversalForwardOnly"),
                               new ShaderTagId("SRPDefaultUnlit") };
            var desc = new RendererListDesc(tags, rendering.cullResults, camera.camera)
            {
                renderQueueRange = RenderQueueRange.opaque,
                sortingCriteria = SortingCriteria.CommonOpaque,
                layerMask = layers,
                overrideMaterial = material,
                overrideMaterialPassIndex = 0
            };
            using (var builder = graph.AddRasterRenderPass<PassData>("E07 Inverted Hull",out var data))
            {
                data.list = graph.CreateRendererList(desc);
                builder.UseRendererList(data.list);
                builder.SetRenderAttachment(resources.activeColorTexture,0,AccessFlags.ReadWrite);
                builder.SetRenderAttachmentDepth(resources.activeDepthTexture,AccessFlags.Read);
                builder.SetRenderFunc(static (PassData p,RasterGraphContext ctx) => ctx.cmd.DrawRendererList(p.list));
            }
        }
    }
}
