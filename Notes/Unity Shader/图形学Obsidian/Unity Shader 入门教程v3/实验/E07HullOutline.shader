Shader "Encyclopedia/E07HullOutline"
{
    Properties
    {
        _OutlineColor("Outline Color", Color) = (0.02,0.01,0.04,1)
        [Enum(Object,0,World,1,Pixels,2)] _WidthMode("Width Space", Float) = 2
        [Enum(Normal,0,Radial,1)] _Direction("Extrusion Direction", Float) = 0
        _WidthOS("Object Width", Range(0,0.2)) = 0.03
        _WidthWS("World Width", Range(0,0.2)) = 0.03
        _WidthPixels("Target Pixel Offset", Range(0,12)) = 3
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" }
        Pass
        {
            Name "E07Hull"
            Cull Front ZWrite Off ZTest LEqual Blend Off
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            CBUFFER_START(UnityPerMaterial)
                float4 _OutlineColor;
                float _WidthMode, _Direction, _WidthOS, _WidthWS, _WidthPixels;
            CBUFFER_END
            struct Attributes { float4 positionOS : POSITION; float3 normalOS : NORMAL; };
            struct Varyings { float4 positionCS : SV_POSITION; };
            Varyings Vert(Attributes i)
            {
                Varyings o;
                float3 dirOS = i.normalOS;
                if (_Direction > 0.5 && dot(i.positionOS.xyz,i.positionOS.xyz) > 1e-8)
                    dirOS = normalize(i.positionOS.xyz);
                float3 p = TransformObjectToWorld(i.positionOS.xyz);
                float3 dirWS = _Direction < 0.5 ? TransformObjectToWorldNormal(dirOS) :
                                                TransformObjectToWorldDir(dirOS,true);
                if (_WidthMode < 0.5)
                    o.positionCS = TransformObjectToHClip(i.positionOS.xyz + normalize(dirOS)*_WidthOS);
                else if (_WidthMode < 1.5)
                    o.positionCS = TransformWorldToHClip(p + dirWS*_WidthWS);
                else
                {
                    float4 c = TransformWorldToHClip(p);
                    float4 probe = TransformWorldToHClip(p + dirWS*0.01);
                    if (c.w > 1e-5 && probe.w > 1e-5)
                    {
                        float2 pixelDir = (probe.xy/probe.w - c.xy/c.w) * 0.5 * _ScaledScreenParams.xy;
                        float len2 = dot(pixelDir,pixelDir);
                        if (len2 > 1e-8)
                        {
                            pixelDir *= rsqrt(len2);
                            c.xy += pixelDir * (2*_WidthPixels/_ScaledScreenParams.xy) * c.w;
                        }
                    }
                    o.positionCS = c;
                }
                return o;
            }
            float4 Frag(Varyings i) : SV_Target { return _OutlineColor; }
            ENDHLSL
        }
    }
}
