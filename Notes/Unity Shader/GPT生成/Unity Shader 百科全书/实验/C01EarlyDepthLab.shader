Shader "Encyclopedia/C01EarlyDepthLab"
{
    Properties
    {
        [KeywordEnum(Opaque,Clip,Depth)] _Variant("Variant",Float)=0
        _Cutoff("UV Clip Threshold",Range(0,1))=0.5
        _Seed("Work Seed",Float)=0.37
        _RawDepthOffset("Raw Depth Offset",Range(-0.01,0.01))=0
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "Queue"="Geometry" }
        Pass
        {
            Tags { "LightMode"="SRPDefaultUnlit" }
            Cull Off ZWrite On ZTest LEqual Blend Off
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            #pragma shader_feature_local _VARIANT_OPAQUE _VARIANT_CLIP _VARIANT_DEPTH
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            CBUFFER_START(UnityPerMaterial)
                float _Variant, _Cutoff, _Seed, _RawDepthOffset;
            CBUFFER_END
            struct Attributes { float3 positionOS:POSITION; float2 uv:TEXCOORD0; };
            struct Varyings { float4 positionCS:SV_POSITION; float2 uv:TEXCOORD0; };
            struct Output
            {
                float4 color:SV_Target;
                #if defined(_VARIANT_DEPTH)
                    float depth:SV_Depth;
                #endif
            };
            Varyings Vert(Attributes input)
            {
                Varyings o;
                o.positionCS=TransformObjectToHClip(input.positionOS);
                o.uv=input.uv;
                return o;
            }
            Output Frag(Varyings input)
            {
                #if defined(_VARIANT_CLIP)
                    clip(input.uv.x-_Cutoff);
                #endif
                float v=input.uv.x+input.uv.y+_Seed;
                [unroll] for(int i=0;i<24;i++)
                    v=frac(v*1.371+0.173);
                Output o;
                o.color=float4(v,0.25+0.5*v,1-v,1);
                #if defined(_VARIANT_DEPTH)
                    o.depth=saturate(input.positionCS.z+_RawDepthOffset);
                #endif
                return o;
            }
            ENDHLSL
        }
    }
}
