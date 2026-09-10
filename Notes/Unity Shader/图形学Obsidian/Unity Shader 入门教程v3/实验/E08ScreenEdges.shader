Shader "Encyclopedia/E08ScreenEdges"
{
    Properties
    {
        [Enum(Composite,0,Depth,1,Normal,2,IdEdges,3,IdData,4)] _View("View", Float) = 0
        _DepthThreshold("Relative Depth Threshold", Range(0.001,0.2)) = 0.02
        _NormalThreshold("One Minus Normal Dot", Range(0.01,1)) = 0.15
        _Radius("Neighbor Radius In Pixels", Range(1,4)) = 1
        _EdgeColor("Edge Color", Color) = (0.02,0.01,0.03,1)
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" }
        Pass
        {
            Cull Off ZWrite Off ZTest Always
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            #pragma multi_compile_fragment _ _GBUFFER_NORMALS_OCT
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Packing.hlsl"
            #include "Packages/com.unity.render-pipelines.core/Runtime/Utilities/Blit.hlsl"
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/DeclareDepthTexture.hlsl"
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/DeclareNormalsTexture.hlsl"
            TEXTURE2D_X_FLOAT(_E08IdTexture);
            CBUFFER_START(UnityPerMaterial)
                float4 _EdgeColor;
                float _View,_DepthThreshold,_NormalThreshold,_Radius;
            CBUFFER_END
            struct SurfaceDataE08
            {
                float z, id, surface, normalValid;
                float3 normal;
            };
            SurfaceDataE08 ReadSurface(float2 uv)
            {
                SurfaceDataE08 o;
                float2 halfTexel=0.5/_ScaledScreenParams.xy;
                uv=clamp(uv,halfTexel,1-halfTexel);
                float raw=SampleSceneDepth(uv);
                #if UNITY_REVERSED_Z
                    o.surface=raw>1e-6 ? 1 : 0;
                #else
                    o.surface=raw<1-1e-6 ? 1 : 0;
                #endif
                o.z=LinearEyeDepth(raw,_ZBufferParams);
                o.normal=SampleSceneNormals(uv);
                float len2=dot(o.normal,o.normal);
                o.normalValid=len2>0.1 ? 1 : 0;
                o.normal*=rsqrt(max(len2,1e-8));
                o.id=round(SAMPLE_TEXTURE2D_X(_E08IdTexture,sampler_PointClamp,uv).r*255.0);
                return o;
            }
            float4 Frag(Varyings i) : SV_Target
            {
                SurfaceDataE08 a=ReadSurface(i.texcoord);
                float ed=0,en=0,ei=0;
                const float2 offsets[4]={float2(1,0),float2(-1,0),float2(0,1),float2(0,-1)};
                [unroll] for(int k=0;k<4;++k)
                {
                    SurfaceDataE08 b=ReadSurface(i.texcoord+offsets[k]*_Radius/_ScaledScreenParams.xy);
                    if(a.surface!=b.surface) ed=1;
                    else if(a.surface>0.5 && b.surface>0.5)
                    {
                        float diff=abs(a.z-b.z)/max(min(a.z,b.z),0.001);
                        ed=max(ed,step(_DepthThreshold,diff));
                        if(a.normalValid>0.5 && b.normalValid>0.5)
                            en=max(en,step(_NormalThreshold,1-clamp(dot(a.normal,b.normal),-1,1)));
                    }
                    ei=max(ei,step(0.5,abs(a.id-b.id)));
                }
                if(_View>3.5)
                {
                    float3 c=a.id<0.5 ? float3(0,0,0) :
                             a.id<1.5 ? float3(1,0.2,0.2) : float3(0.2,1,0.2);
                    return float4(c,1);
                }
                if(_View>0.5)
                {
                    float edge=_View<1.5 ? ed : _View<2.5 ? en : ei;
                    return float4(edge.xxx,1);
                }
                float4 scene=SAMPLE_TEXTURE2D_X(_BlitTexture,sampler_LinearClamp,i.texcoord);
                float combined=max(ed,max(en,ei));
                return float4(lerp(scene.rgb,_EdgeColor.rgb,combined*saturate(_EdgeColor.a)),scene.a);
            }
            ENDHLSL
        }
    }
}
