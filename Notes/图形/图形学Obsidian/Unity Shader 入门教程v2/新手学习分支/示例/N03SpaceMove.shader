Shader "BeginnerNPR/N03SpaceMove"
{
    Properties
    {
        _Distance("Distance",Range(0,0.5))=0.5
        [Toggle] _WorldSpace("World Space Move",Float)=1
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" }
        Pass
        {
            Tags { "LightMode"="SRPDefaultUnlit" }
            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            CBUFFER_START(UnityPerMaterial)
                float _Distance, _WorldSpace;
            CBUFFER_END
            struct Input { float3 positionOS : POSITION; };
            struct Output { float4 positionCS : SV_POSITION; };
            Output Vert(Input input)
            {
                Output output;
                if(_WorldSpace > 0.5)
                {
                    float3 positionWS = TransformObjectToWorld(input.positionOS);
                    positionWS += float3(_Distance,0,0);
                    output.positionCS = TransformWorldToHClip(positionWS);
                }
                else
                {
                    float3 positionOS = input.positionOS + float3(_Distance,0,0);
                    output.positionCS = TransformObjectToHClip(positionOS);
                }
                return output;
            }
            float4 Frag() : SV_Target { return float4(1,0.6,0.1,1); }
            ENDHLSL
        }
    }
}
