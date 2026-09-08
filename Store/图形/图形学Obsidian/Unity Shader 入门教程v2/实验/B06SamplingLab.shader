Shader "Encyclopedia/B06SamplingLab"
{
    Properties
    {
        _MainTex("Checker",2D)="white" {}
        _Mode("Mode",Float)=0
        _Tiling("Tiling",Float)=8
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" }
        Pass
        {
            Tags { "LightMode"="UniversalForward" }
            Cull Off
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            TEXTURE2D(_MainTex); SAMPLER(sampler_MainTex);
            CBUFFER_START(UnityPerMaterial)
                float _Mode, _Tiling;
            CBUFFER_END
            struct A { float3 p:POSITION; float2 uv:TEXCOORD0; };
            struct V { float4 p:SV_POSITION; float2 uv:TEXCOORD0; };
            V Vert(A input)
            {
                V o;
                o.p=TransformObjectToHClip(input.p);
                o.uv=input.uv*_Tiling;
                return o;
            }
            half4 Frag(V input):SV_Target
            {
                float2 gx=ddx(input.uv), gy=ddy(input.uv);
                if(_Mode<0.5) return SAMPLE_TEXTURE2D(_MainTex,sampler_MainTex,input.uv);
                if(_Mode<1.5) return SAMPLE_TEXTURE2D_LOD(_MainTex,sampler_MainTex,input.uv,0);
                if(_Mode<2.5) return SAMPLE_TEXTURE2D(_MainTex,sampler_MainTex,frac(input.uv));
                return SAMPLE_TEXTURE2D_GRAD(_MainTex,sampler_MainTex,frac(input.uv),gx,gy);
            }
            ENDHLSL
        }
    }
}
