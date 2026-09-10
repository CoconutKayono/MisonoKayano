Shader "Encyclopedia/E06MaterialResponse"
{
    Properties
    {
        [Enum(ToonSpecular,0,Strand,1,MatCap,2)] _Mode("Response", Float) = 0
        _BaseColor("Base Color", Color) = (0.12,0.08,0.03,1)
        [HDR] _SpecColor("Highlight Color", Color) = (1,0.65,0.2,1)
        _SpecThreshold("NdotH Threshold", Range(0,1)) = 0.95
        _SpecFeather("Threshold Half Width", Range(0.001,0.1)) = 0.01
        _Exponent("Strand Exponent", Range(1,128)) = 40
        _Shift("Strand Axis Shift", Range(-1,1)) = 0.2
        [Toggle] _FlowAlongV("Use V As Flow Direction", Float) = 1
        _HighlightMask("Highlight Mask (data)", 2D) = "white" {}
        _MatCap("Linear Runtime MatCap", 2D) = "gray" {}
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" "Queue"="Geometry" }
        Pass
        {
            Tags { "LightMode"="UniversalForward" }
            Cull Back ZWrite On ZTest LEqual
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
            TEXTURE2D(_HighlightMask); SAMPLER(sampler_HighlightMask);
            TEXTURE2D(_MatCap); SAMPLER(sampler_MatCap);
            CBUFFER_START(UnityPerMaterial)
                float4 _BaseColor, _SpecColor;
                float _Mode, _SpecThreshold, _SpecFeather, _Exponent, _Shift, _FlowAlongV;
            CBUFFER_END
            struct Attributes
            {
                float4 positionOS : POSITION;
                float3 normalOS : NORMAL;
                float4 tangentOS : TANGENT;
                float2 uv : TEXCOORD0;
            };
            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float3 positionWS : TEXCOORD0;
                float3 normalWS : TEXCOORD1;
                float4 tangentWS : TEXCOORD2;
                float2 uv : TEXCOORD3;
            };
            Varyings Vert(Attributes i)
            {
                Varyings o;
                o.positionWS = TransformObjectToWorld(i.positionOS.xyz);
                o.positionCS = TransformWorldToHClip(o.positionWS);
                o.normalWS = TransformObjectToWorldNormal(i.normalOS);
                o.tangentWS = float4(TransformObjectToWorldDir(i.tangentOS.xyz, false),
                                    i.tangentOS.w * GetOddNegativeScale());
                o.uv = i.uv;
                return o;
            }
            float4 Frag(Varyings i) : SV_Target
            {
                float3 n = normalize(i.normalWS);
                if (_Mode > 1.5)
                {
                    float3 nv = TransformWorldToViewDir(n,true);
                    return float4(SAMPLE_TEXTURE2D(_MatCap,sampler_MatCap,nv.xy*0.5+0.5).rgb,1);
                }
                Light light = GetMainLight();
                float3 v = GetWorldSpaceNormalizeViewDir(i.positionWS);
                float3 sum = light.direction + v;
                float validH = dot(sum,sum) > 1e-8 ? 1 : 0;
                float3 h = sum * rsqrt(max(dot(sum,sum),1e-8));
                float spec;
                if (_Mode < 0.5)
                {
                    spec = smoothstep(_SpecThreshold-_SpecFeather,
                                      _SpecThreshold+_SpecFeather,saturate(dot(n,h)));
                }
                else
                {
                    float3 tangent = i.tangentWS.xyz - n * dot(n,i.tangentWS.xyz);
                    if (dot(tangent,tangent) < 1e-8 || abs(i.tangentWS.w) < 0.5)
                        return float4(1,0,1,1);
                    tangent = normalize(tangent);
                    float3 bitangent = normalize(cross(n,tangent)) * i.tangentWS.w;
                    float3 flow = _FlowAlongV > 0.5 ? bitangent : tangent;
                    flow = normalize(flow + _Shift*n);
                    float th = dot(flow,h);
                    spec = pow(sqrt(saturate(1-th*th)),_Exponent);
                }
                float mask = SAMPLE_TEXTURE2D(_HighlightMask,sampler_HighlightMask,i.uv).r;
                float nl = saturate(dot(n,light.direction));
                float baseBand = lerp(0.3,1.0,step(0.5,nl));
                float3 directSpec = _SpecColor.rgb * spec * mask * validH * nl *
                                    light.color * light.distanceAttenuation;
                return float4(_BaseColor.rgb * baseBand + directSpec,1);
            }
            ENDHLSL
        }
    }
}
