Shader "Encyclopedia/D03Posterize"
{
    Properties { _Levels("Levels Per RGB Channel",Range(2,8))=4 }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" }
        Pass
        {
            ZWrite Off ZTest Always Cull Off Blend Off
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "Packages/com.unity.render-pipelines.core/Runtime/Utilities/Blit.hlsl"
            CBUFFER_START(UnityPerMaterial)
                float _Levels;
            CBUFFER_END
            float4 Frag(Varyings input):SV_Target
            {
                float4 c=SAMPLE_TEXTURE2D_X(_BlitTexture,sampler_LinearClamp,input.texcoord);
                float steps=max(2,floor(_Levels+0.5))-1;
                c.rgb=floor(saturate(c.rgb)*steps+0.5)/steps;
                return c;
            }
            ENDHLSL
        }
    }
}
