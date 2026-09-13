using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.RenderGraphModule;
using UnityEngine.Rendering.Universal;

public class D05CameraDataFeature : ScriptableRendererFeature
{
    public enum View { Depth, Normals, Motion }
    public View view;
    public Material displayMaterial;
    DataPass pass;
    public override void Create()
    {
        pass = new DataPass { renderPassEvent = RenderPassEvent.AfterRenderingPostProcessing };
    }
    public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData data)
    {
        if (displayMaterial == null || !displayMaterial.shader.isSupported) return;
        if (data.cameraData.cameraType != CameraType.Game ||
            data.cameraData.renderType != CameraRenderType.Base) return;
        pass.material = displayMaterial;
        pass.view = view;
        pass.ConfigureInput(view == View.Depth ? ScriptableRenderPassInput.Depth :
            view == View.Normals ? ScriptableRenderPassInput.Normal : ScriptableRenderPassInput.Motion);
        renderer.EnqueuePass(pass);
    }
    class DataPass : ScriptableRenderPass
    {
        public Material material;
        public View view;
        class PassData
        {
            public TextureHandle source;
            public Material material;
            public int shaderPass;
        }
        public override void RecordRenderGraph(RenderGraph graph, ContextContainer frameData)
        {
            var resources = frameData.Get<UniversalResourceData>();
            if (resources.isActiveTargetBackBuffer) return;
            TextureHandle source = view == View.Depth ? resources.cameraDepthTexture :
                view == View.Normals ? resources.cameraNormalsTexture : resources.motionVectorColor;
            if (!source.IsValid()) return;
            var desc = graph.GetTextureDesc(resources.activeColorTexture);
            desc.name = "D05 Camera Data Display";
            desc.depthBufferBits = DepthBits.None;
            desc.msaaSamples = MSAASamples.None;
            desc.bindTextureMS = false;
            desc.clearBuffer = false;
            var output = graph.CreateTexture(desc);
            using (var builder = graph.AddRasterRenderPass<PassData>("D05 " + view, out var p))
            {
                p.source = source;
                p.material = material;
                p.shaderPass = (int)view;
                builder.UseTexture(source, AccessFlags.Read);
                builder.SetRenderAttachment(output, 0, AccessFlags.WriteAll);
                builder.SetRenderFunc(static (PassData d, RasterGraphContext ctx) =>
                    Blitter.BlitTexture(ctx.cmd, d.source, new Vector4(1, 1, 0, 0), d.material, d.shaderPass));
            }
            resources.cameraColor = output;
        }
    }
}
