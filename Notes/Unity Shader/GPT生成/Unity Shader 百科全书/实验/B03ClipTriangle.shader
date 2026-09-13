Shader "Encyclopedia/B03ClipTriangle"
{
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" }
        Pass
        {
            Cull Off
            ZWrite Off
            ZTest Always
            Blend Off
            HLSLPROGRAM
            #pragma target 3.0
            #pragma vertex Vert
            #pragma fragment Frag
            float4 Vert(float3 position:POSITION):SV_POSITION
            {
                return float4(position,1);
            }
            float4 Frag():SV_Target
            {
                return float4(0.1,0.7,0.3,1);
            }
            ENDHLSL
        }
    }
}
