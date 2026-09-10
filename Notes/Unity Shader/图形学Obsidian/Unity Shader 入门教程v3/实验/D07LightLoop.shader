Shader "Encyclopedia/D07LightLoop"
{
    Properties
    {
        _BaseColor("Base Color", Color) = (0.18,0.18,0.18,1)
        [Toggle] _ShowVisits("Show Additional Loop Visits / 16", Float) = 0
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" "Queue"="Geometry" }
        Pass
        {
            Name "D07Forward"
            Tags { "LightMode"="UniversalForward" }
            Cull Back ZWrite On ZTest LEqual
            HLSLPROGRAM
            #pragma target 4.5
            #pragma vertex Vert
            #pragma fragment Frag
            #pragma multi_compile _ _ADDITIONAL_LIGHTS
            #pragma multi_compile _ _CLUSTER_LIGHT_LOOP
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/CommonMaterial.hlsl"
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/RealtimeLights.hlsl"
            CBUFFER_START(UnityPerMaterial)
                float4 _BaseColor;
                float _ShowVisits;
            CBUFFER_END
            struct Attributes
            {
                float4 positionOS : POSITION;
                float3 normalOS : NORMAL;
            };
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
            float3 EvaluateLight(float3 n, Light light)
            {
                return light.color * light.distanceAttenuation * light.shadowAttenuation *
                       saturate(dot(n, light.direction));
            }
            float4 Frag(Varyings i) : SV_Target
            {
                InputData inputData = (InputData)0;
                inputData.positionWS = i.positionWS;
                inputData.normalWS = normalize(i.normalWS);
                inputData.viewDirectionWS = GetWorldSpaceNormalizeViewDir(i.positionWS);
                inputData.normalizedScreenSpaceUV = GetNormalizedScreenSpaceUV(i.positionCS);
                float3 lighting = EvaluateLight(inputData.normalWS, GetMainLight());
                uint visits = 0;
                #if defined(_ADDITIONAL_LIGHTS)
                    #if USE_CLUSTER_LIGHT_LOOP
                        UNITY_LOOP for (uint lightIndex = 0;
                            lightIndex < min(URP_FP_DIRECTIONAL_LIGHTS_COUNT, MAX_VISIBLE_LIGHTS);
                            ++lightIndex)
                        {
                            Light light = GetAdditionalLight(lightIndex, inputData.positionWS, half4(1,1,1,1));
                            lighting += EvaluateLight(inputData.normalWS, light);
                            ++visits;
                        }
                    #endif
                    uint pixelLightCount = GetAdditionalLightsCount();
                    LIGHT_LOOP_BEGIN(pixelLightCount)
                        Light light = GetAdditionalLight(lightIndex, inputData.positionWS, half4(1,1,1,1));
                        lighting += EvaluateLight(inputData.normalWS, light);
                        ++visits;
                    LIGHT_LOOP_END
                #endif
                if (_ShowVisits > 0.5)
                {
                    float value = saturate(visits / 16.0);
                    return float4(value, value, value, 1);
                }
                return float4(_BaseColor.rgb * lighting, 1);
            }
            ENDHLSL
        }
    }
}
