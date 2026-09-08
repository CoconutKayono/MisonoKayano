Shader "Encyclopedia/C08WorkloadLab"
{
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" }
        Pass
        {
            Cull Off ZWrite Off ZTest Always Blend One One
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            float _Contribution;
            int _Iterations;
            float4 Vert(float3 p:POSITION):SV_POSITION { return float4(p.xy,0.5,1); }
            float4 Frag(float4 p:SV_POSITION):SV_Target
            {
                float v=frac(p.x*0.0021+p.y*0.0013);
                [loop] for(int i=0;i<_Iterations;i++) v=frac(v*1.371+0.173);
                return float4(0.1+0.6*v,0.2+0.3*v,0.7-0.4*v,1)*_Contribution;
            }
            ENDHLSL
        }
    }
}
