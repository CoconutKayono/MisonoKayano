Shader "Encyclopedia/E05NormalStreams"
{
    Properties
    {
        [Enum(Original,0,Smooth,1,Edited,2)] _Source("Normal Source", Float) = 0
        [Enum(NormalRGB,0,TwoBands,1)] _View("View", Float) = 0
        _Threshold("Half Lambert Threshold", Range(0,1)) = 0.5
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" "Queue"="Geometry" }
        Pass
        {
            Tags { "LightMode"="UniversalForward" }
            Cull Back ZWrite On ZTest LEqual
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
            CBUFFER_START(UnityPerMaterial)
                float _Source, _View, _Threshold;
            CBUFFER_END
            struct Attributes
            {
                float4 positionOS : POSITION;
                float3 normalOS : NORMAL;
                float3 artisticOS : TEXCOORD2;
                float3 smoothOS : TEXCOORD3;
            };
            struct Varyings { float4 positionCS : SV_POSITION; float3 normalWS : TEXCOORD0; };
            Varyings Vert(Attributes i)
            {
                Varyings o;
                float3 n = _Source < 0.5 ? i.normalOS :
                           _Source < 1.5 ? i.smoothOS : i.artisticOS;
                if (dot(n,n) < 1e-8) n = i.normalOS;
                o.normalWS = TransformObjectToWorldNormal(n);
                o.positionCS = TransformObjectToHClip(i.positionOS.xyz);
                return o;
            }
            float4 Frag(Varyings i) : SV_Target
            {
                float3 n = normalize(i.normalWS);
                float3 color = n * 0.5 + 0.5;
                if (_View > 0.5)
                {
                    Light light = GetMainLight();
                    float q = saturate(0.5 * dot(n,light.direction) + 0.5);
                    color = lerp(float3(0.1,0.12,0.22), float3(1,0.7,0.4), step(_Threshold,q));
                }
                return float4(color,1);
            }
            ENDHLSL
        }
    }
}
