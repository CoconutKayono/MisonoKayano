Shader "Encyclopedia/A01VectorLab"
{
    Properties
    {
        _LightDirectionWS("Surface To Light (World)", Vector) = (0,0,1,0)
        _NormalScale("Normal Length Multiplier", Range(0.1,3)) = 1
        _Threshold("Band Threshold", Range(0,1)) = 0.5
        [Toggle] _NormalizeInput("Normalize Normal", Float) = 1
        [Toggle] _ShowBands("Show Two Bands", Float) = 1
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" "Queue"="Geometry" }
        Pass
        {
            Tags { "LightMode"="UniversalForward" }
            Cull Back
            ZTest LEqual
            ZWrite On
            Blend Off
            HLSLPROGRAM
            #pragma target 3.0
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            CBUFFER_START(UnityPerMaterial)
                float4 _LightDirectionWS;
                float _NormalScale;
                float _Threshold;
                float _NormalizeInput;
                float _ShowBands;
            CBUFFER_END
            struct Attributes
            {
                float3 positionOS : POSITION;
                float3 normalOS : NORMAL;
            };
            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float3 normalWS : TEXCOORD0;
            };
            float3 UnitOrZ(float3 v)
            {
                float lenSq = dot(v,v);
                if (lenSq < 1e-8) return float3(0,0,1);
                return v * rsqrt(lenSq);
            }
            Varyings Vert(Attributes input)
            {
                Varyings o;
                o.positionCS = TransformObjectToHClip(input.positionOS);
                o.normalWS = TransformObjectToWorldNormal(input.normalOS);
                return o;
            }
            half4 Frag(Varyings input) : SV_Target
            {
                // 先统一基线长度，再故意引入可控的长度错误。
                float3 n = UnitOrZ(input.normalWS) * _NormalScale;
                if (_NormalizeInput > 0.5) n = UnitOrZ(n);
                float3 l = UnitOrZ(_LightDirectionWS.xyz);
                float x = saturate(dot(n,l));
                float value = (_ShowBands > 0.5) ? step(_Threshold,x) : x;
                return half4(value,value,value,1);
            }
            ENDHLSL
        }
    }
}
