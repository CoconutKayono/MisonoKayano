Shader "Encyclopedia/B07DepthLab"
{
    Properties
    {
        _Color("Color",Color)=(1,0,0,1)
        [Enum(UnityEngine.Rendering.CompareFunction)] _ZTest("ZTest",Float)=4
        [Enum(Off,0,On,1)] _ZWrite("ZWrite",Float)=1
        [Enum(Color,0,IncomingRawDepth,1,IncomingEyeDepth,2)] _View("View",Float)=0
        _EyeRange("Eye Depth Display Range",Float)=10
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" "Queue"="Geometry" }
        Pass
        {
            Tags { "LightMode"="UniversalForward" }
            ZTest [_ZTest]
            ZWrite [_ZWrite]
            Blend Off
            HLSLPROGRAM
            #pragma target 3.0
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            CBUFFER_START(UnityPerMaterial)
                float4 _Color;
                float _ZTest, _ZWrite, _View, _EyeRange;
            CBUFFER_END
            float4 Vert(float3 position:POSITION):SV_POSITION
            {
                return TransformObjectToHClip(position);
            }
            half4 Frag(float4 position:SV_POSITION):SV_Target
            {
                if(_View<0.5) return _Color;
                float value=position.z;
                if(_View>1.5)
                    value=LinearEyeDepth(position.z,_ZBufferParams)/max(_EyeRange,1e-4);
                return half4(saturate(value),saturate(value),saturate(value),1);
            }
            ENDHLSL
        }
    }
}
