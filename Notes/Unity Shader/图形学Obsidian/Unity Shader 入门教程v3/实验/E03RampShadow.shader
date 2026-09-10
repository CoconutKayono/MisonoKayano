Shader "Encyclopedia/E03RampShadow"
{
    Properties
    {
        _Ramp("Linear Color Ramp", 2D) = "white" {}
        _CastShadowColor("Cast Shadow Color", Color) = (0.08,0.05,0.15,1)
        [Enum(RampThenMultiply,0,MultiplyThenRamp,1,ShadowColorOverride,2,DirectionSignal,3,Visibility,4)]
        _Mode("Composition", Float) = 0
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" "Queue"="Geometry" }
        Pass
        {
            Name "E03Forward"
            Tags { "LightMode"="UniversalForward" }
            Cull Back ZWrite On ZTest LEqual
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            #pragma multi_compile _ _MAIN_LIGHT_SHADOWS _MAIN_LIGHT_SHADOWS_CASCADE
            #pragma multi_compile_fragment _ _SHADOWS_SOFT _SHADOWS_SOFT_LOW _SHADOWS_SOFT_MEDIUM _SHADOWS_SOFT_HIGH
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
            TEXTURE2D(_Ramp);
            SAMPLER(sampler_Ramp);
            CBUFFER_START(UnityPerMaterial)
                float4 _Ramp_TexelSize;
                float4 _CastShadowColor;
                float _Mode;
            CBUFFER_END
            struct Attributes { float4 positionOS : POSITION; float3 normalOS : NORMAL; };
            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float3 positionWS : TEXCOORD0;
                float3 normalWS : TEXCOORD1;
            };
            Varyings Vert(Attributes i)
            {
                Varyings o;
                o.positionWS = TransformObjectToWorld(i.positionOS.xyz);
                o.positionCS = TransformWorldToHClip(o.positionWS);
                o.normalWS = TransformObjectToWorldNormal(i.normalOS);
                return o;
            }
            float3 Ramp(float q)
            {
                float edge = 0.5 * _Ramp_TexelSize.x;
                float u = lerp(edge, 1.0 - edge, saturate(q));
                return SAMPLE_TEXTURE2D(_Ramp, sampler_Ramp, float2(u,0.5)).rgb;
            }
            float4 Frag(Varyings i) : SV_Target
            {
                float4 sc = TransformWorldToShadowCoord(i.positionWS);
                Light light = GetMainLight(sc, i.positionWS, half4(1,1,1,1));
                float q = saturate(0.5 * dot(normalize(i.normalWS), light.direction) + 0.5);
                float s = saturate(light.shadowAttenuation);
                float3 color;
                if (_Mode < 0.5) color = Ramp(q) * s;
                else if (_Mode < 1.5) color = Ramp(q * s);
                else if (_Mode < 2.5) color = lerp(_CastShadowColor.rgb, Ramp(q), s);
                else if (_Mode < 3.5) color = q.xxx;
                else color = s.xxx;
                return float4(color,1);
            }
            ENDHLSL
        }
    }
}
