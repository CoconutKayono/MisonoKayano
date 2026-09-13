Shader "Encyclopedia/E04FaceField"
{
    Properties
    {
        _FaceMap("R Angle Threshold, G Circle SDF, A Face Area", 2D) = "white" {}
        _LitColor("Lit Color", Color) = (1,0.7,0.5,1)
        _ShadeColor("Shade Color", Color) = (0.3,0.13,0.2,1)
        _Feather("Angle Parameter Feather", Range(0,0.1)) = 0.01
        [Enum(Face,0,ThresholdData,1,LightAngle,2,DirectionValidity,3,DistanceContour,4)]
        _View("View", Float) = 0
        [HideInInspector] _HeadRightWS("Head Right", Vector) = (1,0,0,0)
        [HideInInspector] _HeadForwardWS("Head Forward", Vector) = (0,0,1,0)
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" "Queue"="Geometry" }
        Pass
        {
            Name "E04Forward"
            Tags { "LightMode"="UniversalForward" }
            Cull Off ZWrite On ZTest LEqual
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
            TEXTURE2D(_FaceMap);
            SAMPLER(sampler_FaceMap);
            CBUFFER_START(UnityPerMaterial)
                float4 _LitColor, _ShadeColor, _HeadRightWS, _HeadForwardWS;
                float _Feather, _View;
            CBUFFER_END
            struct Attributes { float4 positionOS : POSITION; float2 uv : TEXCOORD0; };
            struct Varyings { float4 positionCS : SV_POSITION; float2 uv : TEXCOORD0; };
            Varyings Vert(Attributes i)
            {
                Varyings o;
                o.positionCS = TransformObjectToHClip(i.positionOS.xyz);
                o.uv = i.uv;
                return o;
            }
            float4 Frag(Varyings i) : SV_Target
            {
                float3 l = GetMainLight().direction;
                float2 h = float2(dot(l, _HeadRightWS.xyz), dot(l, _HeadForwardWS.xyz));
                float len2 = dot(h,h);
                bool valid = len2 > 0.0001;
                h = valid ? h * rsqrt(max(len2,0.0001)) : float2(0,1);
                float t = acos(clamp(h.y,-1.0,1.0)) / PI;
                float2 uv = i.uv;
                if (h.x < 0) uv.x = 1.0 - uv.x;
                float4 data = SAMPLE_TEXTURE2D(_FaceMap, sampler_FaceMap, uv);
                float delta = data.r - t;
                float w = max(max(_Feather, fwidth(delta)), 0.0001);
                float mask = smoothstep(-w,w,delta);
                float d = (data.g - 0.5) * 0.5;
                float dw = max(fwidth(d),0.0001);
                float circle = smoothstep(-dw,dw,d);
                float3 color = lerp(_ShadeColor.rgb, _LitColor.rgb, mask);
                if (_View > 0.5 && _View < 1.5) color = data.rrr;
                else if (_View < 2.5 && _View > 1.5) color = t.xxx;
                else if (_View < 3.5 && _View > 2.5)
                    color = valid ? float3(0.5 + 0.5*h.x, 0.5 + 0.5*h.y, 0) : float3(1,0,1);
                else if (_View > 3.5) color = circle.xxx;
                color = lerp(float3(0.03,0.03,0.03), color, data.a);
                return float4(color,1);
            }
            ENDHLSL
        }
    }
}
