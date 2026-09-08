Shader "Encyclopedia/C03MRTLab"
{
    Properties
    {
        [IntRange] _Id("ID",Range(0,255))=128
        [Enum(All,15,None,0)] _ColorMask("Slot 0 Color Mask",Float)=15
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" }
        Pass
        {
            Cull Off ZTest Always ZWrite On Blend Off
            ColorMask [_ColorMask] 0
            ColorMask R 1
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            CBUFFER_START(UnityPerMaterial)
                float _Id, _ColorMask;
            CBUFFER_END
            struct Attributes { float3 position:POSITION; float2 uv:TEXCOORD0; };
            struct Varyings { float4 positionCS:SV_POSITION; float2 uv:TEXCOORD0; };
            struct Output { float4 color:SV_Target0; float4 id:SV_Target1; };
            Varyings Vert(Attributes input)
            {
                Varyings o;
                o.positionCS=float4(input.position.xy,0.5,1);
                o.uv=input.uv;
                return o;
            }
            Output Frag(Varyings input)
            {
                Output o;
                o.color=float4(input.uv,0.2,1);
                o.id=float4(round(_Id)/255.0,0,0,1);
                return o;
            }
            ENDHLSL
        }
    }
}
