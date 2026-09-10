Shader "Encyclopedia/E01LightingBasis"
{
    Properties
    {
        _LitColor("Lit Color", Color) = (1,0.7,0.4,1)
        _ShadeColor("Shade Color", Color) = (0.18,0.12,0.28,1)
        [Enum(Lambert,0,HalfLambert,1)] _Basis("Direction Signal", Float) = 0
        [Enum(Continuous,0,TwoColors,1)] _View("View", Float) = 0
        _Threshold("Threshold", Range(0,1)) = 0.5
        _Feather("Signal Feather Half Width", Range(0,0.3)) = 0.02
        [Toggle] _UseLightColor("Multiply By Main Light Color", Float) = 0
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" "Queue"="Geometry" }
        Pass
        {
            Name "E01Forward"
            Tags { "LightMode"="UniversalForward" }
            Cull Back ZWrite On ZTest LEqual
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
            CBUFFER_START(UnityPerMaterial)
                float4 _LitColor, _ShadeColor;
                float _Basis, _View, _Threshold, _Feather, _UseLightColor;
            CBUFFER_END
            struct Attributes { float4 positionOS : POSITION; float3 normalOS : NORMAL; };
            struct Varyings { float4 positionCS : SV_POSITION; float3 normalWS : TEXCOORD0; };
            Varyings Vert(Attributes i)
            {
                Varyings o;
                o.positionCS = TransformObjectToHClip(i.positionOS.xyz);
                o.normalWS = TransformObjectToWorldNormal(i.normalOS);
                return o;
            }
            float4 Frag(Varyings i) : SV_Target
            {
                Light light = GetMainLight();
                float3 n = normalize(i.normalWS);
                float x = dot(n, light.direction);
                float q = _Basis < 0.5 ? saturate(x) : saturate(0.5 * x + 0.5);
                float w = max(_Feather, 0.00001);
                float m = _Feather <= 0 ? step(_Threshold, q) :
                    smoothstep(_Threshold - w, _Threshold + w, q);
                float3 color = _View < 0.5 ? q.xxx : lerp(_ShadeColor.rgb, _LitColor.rgb, m);
                color *= lerp(float3(1,1,1), light.color * light.distanceAttenuation,
                              saturate(_UseLightColor));
                return float4(color, 1);
            }
            ENDHLSL
        }
    }
}
