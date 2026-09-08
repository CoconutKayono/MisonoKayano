Shader "Encyclopedia/C05LoadStoreLab"
{
    Properties { _Color("Color",Color)=(1,0,0,1) }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" }
        Pass
        {
            Cull Off ZTest Always ZWrite Off Blend Off
            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment Frag
            float4 _Color;
            float4 Vert(float3 p:POSITION):SV_POSITION { return float4(p.xy,0.5,1); }
            float4 Frag():SV_Target { return _Color; }
            ENDHLSL
        }
    }
}
