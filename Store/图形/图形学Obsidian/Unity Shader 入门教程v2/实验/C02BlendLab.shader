Shader "Encyclopedia/C02BlendLab"
{
    Properties
    {
        _Color("Color",Color)=(1,0,0,0.5)
        [Enum(UnityEngine.Rendering.BlendMode)] _SrcBlend("RGB Source Factor",Float)=5
        [Toggle] _Premultiply("Premultiply RGB",Float)=0
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "Queue"="Transparent" "RenderType"="Transparent" }
        Pass
        {
            Tags { "LightMode"="SRPDefaultUnlit" }
            Cull Off ZTest LEqual ZWrite Off
            Blend [_SrcBlend] OneMinusSrcAlpha, One OneMinusSrcAlpha
            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            CBUFFER_START(UnityPerMaterial)
                float4 _Color;
                float _SrcBlend, _Premultiply;
            CBUFFER_END
            struct Attributes { float3 positionOS:POSITION; };
            struct Varyings { float4 positionCS:SV_POSITION; };
            Varyings Vert(Attributes input)
            {
                Varyings o;
                o.positionCS=TransformObjectToHClip(input.positionOS);
                return o;
            }
            float4 Frag(Varyings input):SV_Target
            {
                float4 c=_Color;
                c.rgb*=lerp(1.0,c.a,step(0.5,_Premultiply));
                return c;
            }
            ENDHLSL
        }
    }
}
