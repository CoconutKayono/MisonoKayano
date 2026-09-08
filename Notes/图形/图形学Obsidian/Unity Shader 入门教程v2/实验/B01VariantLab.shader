Shader "Encyclopedia/B01VariantLab"
{
    Properties
    {
        [Toggle(_B01_BANDS)] _Bands("Static Bands", Float) = 0
        _RuntimeBands("Runtime Bands (0 or 1)", Range(0,1)) = 0
        _Threshold("Threshold", Range(0,1)) = 0.5
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" }
        Pass
        {
            Tags { "LightMode"="UniversalForward" }
            HLSLPROGRAM
            #pragma target 3.0
            #pragma vertex Vert
            #pragma fragment Frag
            #pragma shader_feature_local _ _B01_BANDS
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            CBUFFER_START(UnityPerMaterial)
                float _Bands;
                float _RuntimeBands;
                float _Threshold;
            CBUFFER_END
            struct A { float4 p : POSITION; float2 uv : TEXCOORD0; };
            struct V { float4 p : SV_POSITION; float2 uv : TEXCOORD0; };
            V Vert(A input)
            {
                V output;
                output.p = TransformObjectToHClip(input.p.xyz);
                output.uv = input.uv;
                return output;
            }
            half4 Frag(V input) : SV_Target
            {
                float t = saturate(input.uv.x);
                float staticValue = t;
                #if defined(_B01_BANDS)
                    staticValue = step(_Threshold, t);
                #endif
                float runtimeValue = t;
                if (_RuntimeBands > 0.5)
                    runtimeValue = step(_Threshold, t);
                float value = input.uv.y >= 0.5 ? staticValue : runtimeValue;
                return half4(value, value, value, 1);
            }
            ENDHLSL
        }
    }
}
