Shader "Encyclopedia/E08GroupId"
{
    Properties { _Id("Group Id (1 or 2)", Range(1,2)) = 1 }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" }
        Pass
        {
            Cull Back ZWrite Off ZTest LEqual Blend Off
            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            CBUFFER_START(UnityPerMaterial)
                float _Id;
            CBUFFER_END
            struct Attributes { float4 positionOS : POSITION; };
            struct Varyings { float4 positionCS : SV_POSITION; };
            Varyings Vert(Attributes i)
            {
                Varyings o;
                o.positionCS=TransformObjectToHClip(i.positionOS.xyz);
                return o;
            }
            float4 Frag(Varyings i) : SV_Target { return float4(round(_Id)/255.0,0,0,1); }
            ENDHLSL
        }
    }
}
