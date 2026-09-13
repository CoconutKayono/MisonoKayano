Shader "Encyclopedia/C07DeformationLab"
{
    Properties
    {
        _Color("Color",Color)=(0.2,0.7,1,1)
        _Amplitude("Additional Displacement",Range(0,0.5))=0.2
        _Frequency("Frequency",Float)=4
        _Speed("Speed",Float)=2
        [Toggle] _MatchAux("Deform Depth And Shadow",Float)=1
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "Queue"="Geometry" "RenderType"="Opaque" }
        HLSLINCLUDE
        #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
        #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Shadows.hlsl"
        CBUFFER_START(UnityPerMaterial)
            float4 _Color;
            float _Amplitude, _Frequency, _Speed, _MatchAux;
        CBUFFER_END
        float3 _LightDirection, _LightPosition;
        struct Input { float3 positionOS:POSITION; float3 normalOS:NORMAL; };
        struct Output { float4 positionCS:SV_POSITION; };
        float3 Deform(float3 p,float amount)
        {
            p.x+=amount*sin(p.y*_Frequency+_Time.y*_Speed);
            return p;
        }
        float3 DeformNormal(float3 p,float3 n,float amount)
        {
            float k=amount*_Frequency*cos(p.y*_Frequency+_Time.y*_Speed);
            return normalize(float3(n.x,n.y-k*n.x,n.z));
        }
        Output MainVert(Input input)
        {
            Output o;
            o.positionCS=TransformObjectToHClip(Deform(input.positionOS,_Amplitude));
            return o;
        }
        Output DepthVert(Input input)
        {
            Output o;
            o.positionCS=TransformObjectToHClip(Deform(input.positionOS,_Amplitude*step(0.5,_MatchAux)));
            return o;
        }
        Output ShadowVert(Input input)
        {
            float a=_Amplitude*step(0.5,_MatchAux);
            float3 p=TransformObjectToWorld(Deform(input.positionOS,a));
            float3 n=TransformObjectToWorldNormal(DeformNormal(input.positionOS,input.normalOS,a));
            #if defined(_CASTING_PUNCTUAL_LIGHT_SHADOW)
                float3 lightDirection=normalize(_LightPosition-p);
            #else
                float3 lightDirection=_LightDirection;
            #endif
            Output o;
            o.positionCS=ApplyShadowClamping(TransformWorldToHClip(ApplyShadowBias(p,n,lightDirection)));
            return o;
        }
        float4 ColorFrag():SV_Target { return _Color; }
        float4 DepthFrag():SV_Target { return 0; }
        ENDHLSL
        Pass
        {
            Name "Forward"
            Tags { "LightMode"="SRPDefaultUnlit" }
            Cull Off ZWrite On ZTest LEqual
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex MainVert
            #pragma fragment ColorFrag
            ENDHLSL
        }
        Pass
        {
            Name "DepthOnly"
            Tags { "LightMode"="DepthOnly" }
            Cull Off ZWrite On ZTest LEqual ColorMask 0
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex DepthVert
            #pragma fragment DepthFrag
            ENDHLSL
        }
        Pass
        {
            Name "ShadowCaster"
            Tags { "LightMode"="ShadowCaster" }
            Cull Off ZWrite On ZTest LEqual ColorMask 0
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex ShadowVert
            #pragma fragment DepthFrag
            #pragma multi_compile_vertex _ _CASTING_PUNCTUAL_LIGHT_SHADOW
            ENDHLSL
        }
    }
}
