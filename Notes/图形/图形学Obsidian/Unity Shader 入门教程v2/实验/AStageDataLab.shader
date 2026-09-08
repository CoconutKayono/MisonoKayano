Shader "Encyclopedia/AStageDataLab"
{
    Properties
    {
        [Enum(WorldNormal,0,UV,1,WorldPosition,2,NdotL,3,ColorCompare,4)]
        _Mode("View", Float) = 0
        _PositionScale("World Position Scale", Float) = 0.1
        _LightDirection("World Surface To Light", Vector) = (0,1,0,0)
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" "Queue"="Geometry" }
        Pass
        {
            Name "DataView"
            Tags { "LightMode"="UniversalForward" }
            Cull Back
            ZWrite On
            ZTest LEqual
            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

            CBUFFER_START(UnityPerMaterial)
                float4 _LightDirection;
                float _Mode;
                float _PositionScale;
            CBUFFER_END

            struct Attributes
            {
                float4 positionOS : POSITION;
                float3 normalOS : NORMAL;
                float2 uv : TEXCOORD0;
            };
            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float3 positionWS : TEXCOORD0;
                float3 normalWS : TEXCOORD1;
                float2 uv : TEXCOORD2;
            };
            float3 UnitOrZero(float3 v)
            {
                return v * rsqrt(max(dot(v, v), 1e-12));
            }
            float DecodeSRGB01(float e)
            {
                return e <= 0.04045 ? e / 12.92
                    : pow((e + 0.055) / 1.055, 2.4);
            }
            Varyings Vert(Attributes input)
            {
                Varyings output;
                output.positionWS = TransformObjectToWorld(input.positionOS.xyz);
                output.positionCS = TransformWorldToHClip(output.positionWS);
                output.normalWS = TransformObjectToWorldNormal(input.normalOS, false);
                output.uv = input.uv;
                return output;
            }
            half4 Frag(Varyings input) : SV_Target
            {
                float3 n = UnitOrZero(input.normalWS);
                float3 c;
                if (_Mode < 0.5)
                    c = n * 0.5 + 0.5;
                else if (_Mode < 1.5)
                    c = float3(saturate(input.uv), 0);
                else if (_Mode < 2.5)
                    c = saturate(input.positionWS * _PositionScale + 0.5);
                else if (_Mode < 3.5)
                {
                    float value = saturate(dot(n, UnitOrZero(_LightDirection.xyz)));
                    c = float3(value, value, value);
                }
                else
                {
                    float t = saturate(input.uv.x);
                    float value = input.uv.y >= 0.5 ? t : DecodeSRGB01(t);
                    c = float3(value, value, value);
                }
                return half4(c, 1);
            }
            ENDHLSL
        }
    }
}
