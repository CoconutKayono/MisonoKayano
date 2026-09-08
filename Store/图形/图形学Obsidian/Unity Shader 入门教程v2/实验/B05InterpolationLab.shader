Shader "Encyclopedia/B05InterpolationLab"
{
    Properties
    {
        [Enum(PerspectiveUV,0,AffineUV,1,Derivatives,2,Threshold,3)] _Mode("View",Float)=0
        _Threshold("Threshold",Range(0,1))=0.5
        _DerivativeScale("Derivative Display Scale",Float)=32
        _AA("Threshold AA (0 or 1)",Range(0,1))=1
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" }
        Pass
        {
            Tags { "LightMode"="UniversalForward" }
            Cull Off
            HLSLPROGRAM
            #pragma target 3.0
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            CBUFFER_START(UnityPerMaterial)
                float _Mode, _Threshold, _DerivativeScale, _AA;
            CBUFFER_END
            struct A { float3 p:POSITION; float2 uv:TEXCOORD0; };
            struct V {
                float4 p:SV_POSITION;
                float2 uv:TEXCOORD0;
                float3 affinePack:TEXCOORD1;
            };
            V Vert(A input)
            {
                V o;
                o.p=TransformObjectToHClip(input.p);
                o.uv=input.uv;
                o.affinePack=float3(input.uv*o.p.w,o.p.w);
                return o;
            }
            half4 Frag(V input):SV_Target
            {
                float2 affineUV=input.affinePack.xy/input.affinePack.z;
                float dx=ddx(input.uv.x);
                float dy=ddy(input.uv.x);
                float width=max(abs(dx)+abs(dy),1e-5);
                float3 color;
                if(_Mode<0.5) color=float3(input.uv,0);
                else if(_Mode<1.5) color=float3(affineUV,0);
                else if(_Mode<2.5)
                    color=float3(abs(dx),abs(dy),width)*_DerivativeScale;
                else
                {
                    float hard=step(_Threshold,input.uv.x);
                    float soft=smoothstep(_Threshold-width*0.5,
                                         _Threshold+width*0.5,input.uv.x);
                    float value=_AA>0.5 ? soft : hard;
                    color=float3(value,value,value);
                }
                return half4(saturate(color),1);
            }
            ENDHLSL
        }
    }
}
