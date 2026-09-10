Shader "Encyclopedia/D08TraceLab"
{
    Properties
    {
        _Color("Output Color", Color) = (1,0,0,1)
        [Enum(None,0,RGB,14,RGBA,15)] _ColorMask("Color Write Mask", Float) = 15
        [Toggle] _ZWrite("Depth Write", Float) = 1
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" "Queue"="Geometry" }
        Pass
        {
            Name "D08TraceForward"
            Tags { "LightMode"="UniversalForward" }
            Cull Off
            ZTest LEqual
            ZWrite [_ZWrite]
            ColorMask [_ColorMask]
            Blend Off
            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            CBUFFER_START(UnityPerMaterial)
                float4 _Color;
                float _ColorMask;
                float _ZWrite;
            CBUFFER_END
            struct Attributes { float4 positionOS : POSITION; };
            struct Varyings { float4 positionCS : SV_POSITION; };
            Varyings Vert(Attributes i)
            {
                Varyings o;
                o.positionCS = TransformObjectToHClip(i.positionOS.xyz);
                return o;
            }
            float4 Frag(Varyings i) : SV_Target { return _Color; }
            ENDHLSL
        }
    }
}
