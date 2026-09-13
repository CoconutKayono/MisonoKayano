Shader "Encyclopedia/C04CoverageLab"
{
    Properties { _Mask("Alpha Mask",2D)="white" {} }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" }
        HLSLINCLUDE
        #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
        TEXTURE2D(_Mask);
        SAMPLER(sampler_Mask);
        struct Attributes { float3 position:POSITION; float2 uv:TEXCOORD0; };
        struct Varyings { float4 positionCS:SV_POSITION; float2 uv:TEXCOORD0; };
        Varyings Vert(Attributes input)
        {
            Varyings o;
            o.positionCS=float4(input.position.xy,0.5,1);
            o.uv=input.uv;
            return o;
        }
        float4 Frag(Varyings input):SV_Target
        {
            float a=SAMPLE_TEXTURE2D(_Mask,sampler_Mask,input.uv).a;
            return float4(0.15,0.8,0.3,a);
        }
        float4 FragClip(Varyings input):SV_Target
        {
            float4 c=Frag(input);
            clip(c.a-0.5);
            return c;
        }
        ENDHLSL
        Pass
        {
            Name "SolidAlphaIgnored"
            Cull Off ZTest Always ZWrite On Blend Off AlphaToMask Off
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            ENDHLSL
        }
        Pass
        {
            Name "Clip"
            Cull Off ZTest Always ZWrite On Blend Off AlphaToMask Off
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment FragClip
            ENDHLSL
        }
        Pass
        {
            Name "AlphaToCoverage"
            Cull Off ZTest Always ZWrite On Blend Off AlphaToMask On
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            ENDHLSL
        }
        Pass
        {
            Name "AlphaBlend"
            Cull Off ZTest Always ZWrite Off AlphaToMask Off
            Blend SrcAlpha OneMinusSrcAlpha, One OneMinusSrcAlpha
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            ENDHLSL
        }
    }
}
