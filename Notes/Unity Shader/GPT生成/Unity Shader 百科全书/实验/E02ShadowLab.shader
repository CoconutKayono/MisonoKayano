Shader "Encyclopedia/E02ShadowLab"
{
    Properties
    {
        _BaseColor("Base Color", Color) = (0.7,0.7,0.7,1)
        [Enum(Visibility,0,Lambert,1,Cascades,2)] _View("View", Float) = 0
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" "Queue"="Geometry" }
        HLSLINCLUDE
        #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
        CBUFFER_START(UnityPerMaterial)
            float4 _BaseColor;
            float _View;
        CBUFFER_END
        ENDHLSL
        Pass
        {
            Name "E02Forward"
            Tags { "LightMode"="UniversalForward" }
            Cull Back ZWrite On ZTest LEqual
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            #pragma multi_compile _ _MAIN_LIGHT_SHADOWS _MAIN_LIGHT_SHADOWS_CASCADE
            #pragma multi_compile_fragment _ _SHADOWS_SOFT _SHADOWS_SOFT_LOW _SHADOWS_SOFT_MEDIUM _SHADOWS_SOFT_HIGH
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
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
            float4 Frag(Varyings i) : SV_Target
            {
                float4 sc = TransformWorldToShadowCoord(i.positionWS);
                Light light = GetMainLight(sc, i.positionWS, half4(1,1,1,1));
                if (_View < 0.5) return float4(light.shadowAttenuation.xxx, 1);
                if (_View > 1.5)
                {
                    uint cascade = 0;
                    #if defined(_MAIN_LIGHT_SHADOWS_CASCADE)
                        cascade = (uint)ComputeCascadeIndex(i.positionWS);
                    #endif
                    float3 c = cascade == 0 ? float3(1,0.2,0.2) :
                               cascade == 1 ? float3(0.2,1,0.2) :
                               cascade == 2 ? float3(0.2,0.3,1) :
                               cascade == 3 ? float3(1,1,0.2) : float3(0,0,0);
                    return float4(c,1);
                }
                float q = saturate(dot(normalize(i.normalWS), light.direction));
                return float4(_BaseColor.rgb * light.color * light.distanceAttenuation *
                              q * light.shadowAttenuation, 1);
            }
            ENDHLSL
        }
        Pass
        {
            Name "ShadowCaster"
            Tags { "LightMode"="ShadowCaster" }
            Cull Back ZWrite On ZTest LEqual ColorMask 0
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex ShadowVert
            #pragma fragment ShadowFrag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Shadows.hlsl"
            float3 _LightDirection;
            struct Attributes { float4 positionOS : POSITION; float3 normalOS : NORMAL; };
            struct Varyings { float4 positionCS : SV_POSITION; };
            Varyings ShadowVert(Attributes i)
            {
                Varyings o;
                float3 p = TransformObjectToWorld(i.positionOS.xyz);
                float3 n = TransformObjectToWorldNormal(i.normalOS);
                o.positionCS = TransformWorldToHClip(ApplyShadowBias(p, n, _LightDirection));
                #if UNITY_REVERSED_Z
                    o.positionCS.z = min(o.positionCS.z, o.positionCS.w * UNITY_NEAR_CLIP_VALUE);
                #else
                    o.positionCS.z = max(o.positionCS.z, o.positionCS.w * UNITY_NEAR_CLIP_VALUE);
                #endif
                return o;
            }
            float4 ShadowFrag(Varyings i) : SV_Target { return 0; }
            ENDHLSL
        }
    }
}
