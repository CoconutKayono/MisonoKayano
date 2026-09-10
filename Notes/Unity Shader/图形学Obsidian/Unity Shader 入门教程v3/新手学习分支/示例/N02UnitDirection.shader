Shader "BeginnerNPR/N02UnitDirection"
{
    Properties
    {
        _Direction("Direction XYZ",Vector)=(1,0,0,0)
        _Distance("Distance",Range(0,0.5))=0.5
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
                float4 _Direction;
                float _Distance;
            CBUFFER_END
            struct Input { float3 positionOS : POSITION; };
            struct Output { float4 positionCS : SV_POSITION; };
            Output Vert(Input input)
            {
                float3 direction = _Direction.xyz;
                float3 unitDirection = float3(0,0,0);
                if(length(direction) > 0.00001)
                    unitDirection = normalize(direction);
                float3 movedPosition = input.positionOS + unitDirection * _Distance;
                Output output;
                output.positionCS = TransformObjectToHClip(movedPosition);
                return output;
            }
            float4 Frag() : SV_Target { return float4(1,0.6,0.1,1); }
            ENDHLSL
        }
    }
}
