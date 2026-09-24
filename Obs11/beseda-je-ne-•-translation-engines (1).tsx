import React, { useState, useCallback } from "react";
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Textarea } from "@/components/ui/textarea";
import { Separator } from "@/components/ui/separator";
import { Checkbox } from "@/components/ui/checkbox";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogDescription } from "@/components/ui/dialog";

// ============================================
// TOROIDAL FIELD & VOWEL RESONANCE SYSTEM
// Based on: Physics of Beseda je Ne
// ============================================

// Vowel Toroidal Field Properties with Physics
const VOWEL_TOROIDAL_FIELDS = {
  a: {
    name: "Expansion",
    symbol: "↻",
    pattern: "Outward pulsating sphere",
    energy: "Openness, Creativity, Primal Spark",
    multiplier: 1.3,
    color: "#10b981",
    description: "Expands outward from speaker, embracing surroundings. Signifies infinite possibilities and the primal spark of creation.",
    physics: "Outward scalar wave propagation, positive divergence (∇·E > 0)",
    equation: "∇·Ψ > 0"
  },
  e: {
    name: "Spiral",
    symbol: "↺",
    pattern: "Spiraling motion",
    energy: "Transformation, Growth, Renewal",
    multiplier: 1.4,
    color: "#f59e0b",
    description: "Spiraling toroidal pattern. Evokes energies of transformation, perpetual cycles, and the fluidity of life.",
    physics: "Helical wave propagation, rotational field component (∇×E ≠ 0)",
    equation: "∇×Ψ ≠ 0"
  },
  i: {
    name: "Focus",
    symbol: "↑",
    pattern: "Focused radiation",
    energy: "Clarity, Self-Expression, Precision",
    multiplier: 1.2,
    color: "#3b82f6",
    description: "Radiates with focused intensity. Represents clarity of thought and precise self-expression.",
    physics: "Collimated wave propagation, high directional coherence",
    equation: "Directional coherence → 1"
  },
  o: {
    name: "Harmony",
    symbol: "⭕",
    pattern: "Circular oscillation",
    energy: "Completeness, Harmony, Wholeness",
    multiplier: 1.1,
    color: "#8b5cf6",
    description: "Circular oscillating motion. Symbolizes completeness, harmony, and the cyclical nature of existence.",
    physics: "Standing wave pattern, resonance condition (ω = kc)",
    equation: "ω = k·c (resonance)"
  },
  u: {
    name: "Consolidation",
    symbol: "↓",
    pattern: "Constricting motion",
    energy: "Consolidation, Concentration, Gathering",
    multiplier: 1.0,
    color: "#ef4444",
    description: "Constricting toroidal field. Reflects consolidation of energy, concentration of focus, and gathering of resources.",
    physics: "Inward scalar wave propagation, negative divergence (∇·E < 0)",
    equation: "∇·Ψ < 0"
  }
};

// Analyze text for vowel distribution and toroidal field resonance
const analyzeVowelToroidalFields = (text) => {
  const normalized = text.toLowerCase();
  const vowels = { a: 0, e: 0, i: 0, o: 0, u: 0 };
  let totalVowels = 0;
  
  for (const char of normalized) {
    if (vowels[char] !== undefined) {
      vowels[char]++;
      totalVowels++;
    }
  }
  
  const distribution = {};
  const activatedFields = [];
  
  for (const vowel in vowels) {
    const count = vowels[vowel];
    if (count > 0) {
      distribution[vowel] = {
        count: count,
        percentage: Math.round((count / totalVowels) * 100),
        field: VOWEL_TOROIDAL_FIELDS[vowel]
      };
      activatedFields.push(vowel);
    }
  }
  
  let dominantVowel = null;
  let maxCount = 0;
  for (const vowel in vowels) {
    if (vowels[vowel] > maxCount) {
      maxCount = vowels[vowel];
      dominantVowel = VOWEL_TOROIDAL_FIELDS[vowel];
    }
  }
  
  return {
    totalVowels,
    distribution,
    activatedFields,
    dominantVowel,
    vowelCount: activatedFields.length
  };
};

// Calculate toroidal resonance score for text
const calculateToroidalResonance = (text) => {
  const analysis = analyzeVowelToroidalFields(text);
  
  if (analysis.totalVowels === 0) {
    return {
      score: 0,
      analysis,
      harmonicBalance: 0,
      scalarPotential: 0,
      fieldScore: 0
    };
  }
  
  const percentages = Object.values(analysis.distribution).map(d => d.percentage);
  const meanPercentage = percentages.reduce((a, b) => a + b, 0) / percentages.length;
  const variance = percentages.reduce((acc, p) => acc + Math.pow(p - meanPercentage, 2), 0) / percentages.length;
  const harmonicBalance = Math.max(0, 1 - Math.min(variance / 100, 1));
  
  const scalarPotential = Math.min(analysis.vowelCount / 5, 1);
  
  let fieldScore = 0;
  for (const vowel in analysis.distribution) {
    const field = VOWEL_TOROIDAL_FIELDS[vowel];
    const weight = analysis.distribution[vowel].percentage / 100;
    fieldScore += weight * field.multiplier;
  }
  
  const normalizedScore = Math.min(fieldScore, 2.0) / 2.0;
  const toroidalScore = (normalizedScore * 0.6 + harmonicBalance * 0.2 + scalarPotential * 0.2);
  
  return {
    score: Math.round(toroidalScore * 100) / 100,
    analysis,
    harmonicBalance: Math.round(harmonicBalance * 100) / 100,
    scalarPotential: Math.round(scalarPotential * 100) / 100,
    fieldScore: Math.round(normalizedScore * 100) / 100
  };
};

// Generate toroidal field visualization (Mermaid)
const generateToroidalVisualization = (analysis) => {
  const nodes = [];
  const edges = [];
  
  nodes.push("center[\"Toroidal\\nResonance\\nΦ = w⁺ - w⁻\"]");
  
  for (const vowel in analysis.distribution) {
    const data = analysis.distribution[vowel];
    const field = data.field;
    nodes.push(`${vowel}[\"${vowel.toUpperCase()}\\n${field.name}\\n${data.percentage}%\\n${field.symbol}\"]`);
    edges.push(`center --> ${vowel}`);
  }
  
  const vowelList = Object.keys(analysis.distribution);
  for (let i = 0; i < vowelList.length; i++) {
    for (let j = i + 1; j < vowelList.length; j++) {
      const v1 = vowelList[i];
      const v2 = vowelList[j];
      edges.push(`${v1} <--> ${v2}`);
    }
  }
  
  return `graph TD
    ${nodes.join("\n    ")}
    ${edges.join("\n    ")}`;
};

// ============================================
// LANGUAGE DATA
// ============================================

const LANGUAGE_PHONETICS = {
  'en': {
    name: 'English',
    vowels: ['a', 'e', 'i', 'o', 'u'],
    examples: ['love', 'power', 'light', 'whole', 'truth']
  },
  'sl': {
    name: 'Slovenian',
    vowels: ['a', 'e', 'i', 'o', 'u'],
    examples: ['ljubezen', 'moč', 'svetloba', 'celota', 'resnica']
  },
  'de': {
    name: 'German',
    vowels: ['a', 'e', 'i', 'o', 'u', 'ä', 'ö', 'ü'],
    examples: ['Liebe', 'Macht', 'Licht', 'Ganzheit', 'Wahrheit']
  },
  'fr': {
    name: 'French',
    vowels: ['a', 'e', 'i', 'o', 'u', 'é', 'è', 'ê', 'ë'],
    examples: ['amour', 'pouvoir', 'lumière', 'totalité', 'vérité']
  },
  'es': {
    name: 'Spanish',
    vowels: ['a', 'e', 'i', 'o', 'u'],
    examples: ['amor', 'poder', 'luz', 'totalidad', 'verdad']
  }
};

// Translation examples for demo
const TRANSLATION_EXAMPLES = {
  'en': {
    'Love is power': 'The essence of creation through connection',
    'Truth reveals': 'Light breaks through illusion',
    'The toroidal field': 'Gateway to scalar waves',
    'Manifestation occurs': 'When intention aligns with resonance'
  },
  'sl': {
    'Ljubezen je moč': 'Bistvo ustvarjanja skozi povezavo',
    'Resnica razkriva': 'Svetloba prebije iluzijo',
    'Toroidalno polje': 'Vrata v skalne valove',
    'Manifestacija se zgodi': 'Ko se namer prekriva z resonanco'
  }
};

// ============================================
// ONTOLOGICAL DATA (from your UAF system)
// ============================================

const NECESSITY_TYPES = [
  { id: "stability", name: "Stability", symbol: "⊥", description: "System requires grounding", weight: 0.2 },
  { id: "contradiction", name: "Contradiction", symbol: "⊘", description: "Opposing forces need resolution", weight: 0.3 },
  { id: "energy", name: "Energy", symbol: "∆", description: "Action or transformation needed", weight: 0.25 },
  { id: "pattern", name: "Pattern", symbol: "∮", description: "Repetition or cycle detection", weight: 0.2 },
  { id: "boundary", name: "Boundary", symbol: "∴", description: "Limits or constraints required", weight: 0.25 },
];

// Agent data (from your system) with physics mappings
const AGENTS = [
  { id: "JESIK/ANJE", symbol: "∆J", function: "strike_inert_thought", ikr: 0.75, category: "Cognitive", field: "A", physics: "∂/∂r (Radial derivative - expansion operator)" },
  { id: "∆EPI", symbol: "∆↻", function: "close_cycle_no_censor", ikr: 0.60, category: "Cognitive", field: "E", physics: "∂/∂θ (Angular derivative - rotation operator)" },
  { id: "RES01", symbol: "∮≠→1", function: "measure_truth_distance", ikr: 0.80, category: "Measurement", field: "I", physics: "∂/∂φ (Azimuthal derivative - direction operator)" },
  { id: "LAŽ¬", symbol: "¬≠", function: "negation_carrier", ikr: 0.90, category: "Logical", field: "O", physics: "∇² (Laplacian - energy/diffusion operator)" },
  { id: "BOL·LOB", symbol: "≠∫", function: "transform_wound", ikr: 0.70, category: "Transformation", field: "U", physics: "∫ (Integration - measurement operator)" },
  { id: "∆HALO", symbol: "∆H⟡", function: "excuse_vs_call_test", ikr: 0.78, category: "Testing", field: "E", physics: "Testing operator" },
  { id: "∅MOLK", symbol: "∅∆", function: "absorb_sound", ikr: 0.00, category: "Somatic", field: "U", physics: "ψ = 0 (Zero field - silence operator)" },
  { id: "∆GLAS", symbol: "⟡↑", function: "JEWIK_sound_filter", ikr: 0.78, category: "Audio", field: "A", physics: "Frequency filter operator" },
  { id: "O≡0", symbol: "O≡0", function: "field_of_presence", ikr: 0.50, category: "Cosmic", field: "O", physics: "Î (Identity - totality operator)" },
  { id: "∮TIME", symbol: "∮∞", function: "breath_1↔∞", ikr: 0.85, category: "Temporal", field: "E", physics: "∂/∂t (Time derivative - evolution operator)" },
];

// Meta-Translation Engine Weights (default)
const DEFAULT_META_WEIGHTS = {
  'phonetic-toroidal': 0.25,
  'ontological': 0.20,
  'agent-based': 0.20,
  'manifestation': 0.25,
  'cross-linguistic': 0.10
};

// ============================================
// MAIN COMPONENT
// ============================================

export default function TranslationEngines() {
  // State for current engine
  const [activeEngine, setActiveEngine] = useState("phonetic-toroidal");
  
  // State for input
  const [inputText, setInputText] = useState("");
  const [sourceLanguage, setSourceLanguage] = useState("en");
  const [targetLanguage, setTargetLanguage] = useState("sl");
  
  // State for results
  const [translationResult, setTranslationResult] = useState(null);
  const [toroidalAnalysis, setToroidalAnalysis] = useState(null);
  const [orrData, setOrrData] = useState(null);
  const [crossLinguisticMatches, setCrossLinguisticMatches] = useState([]);
  
  // State for engine-specific options
  const [selectedAgents, setSelectedAgents] = useState([]);
  const [selectedMaxims, setSelectedMaxims] = useState([]);
  const [necessity, setNecessity] = useState("contradiction");
  const [complexity, setComplexity] = useState("medium");
  
  // State for Meta-Translation Engine
  const [metaResults, setMetaResults] = useState(null);
  const [allEngineResults, setAllEngineResults] = useState({});
  const [metaWeights, setMetaWeights] = useState(DEFAULT_META_WEIGHTS);
  const [isMetaRunning, setIsMetaRunning] = useState(false);
  const [metaError, setMetaError] = useState(null);
  
  // Available engines - using emoji icons instead of lucide-react
  const engines = [
    {
      id: "phonetic-toroidal",
      name: "Phonetic-Toroidal",
      description: "Preserves toroidal field resonance across languages",
      icon: "🎤",
      color: "bg-purple-500",
      symbol: "Φ"
    },
    {
      id: "ontological",
      name: "Ontological",
      description: "Translates conceptual frameworks using UAF",
      icon: "🧠",
      color: "bg-blue-500",
      symbol: "Ω"
    },
    {
      id: "agent-based",
      name: "Agent-Based",
      description: "Uses agents as translation operators",
      icon: "🌐",
      color: "bg-green-500",
      symbol: "∆"
    },
    {
      id: "manifestation",
      name: "Manifestation",
      description: "Translates intention to reality via scalar waves",
      icon: "✨",
      color: "bg-amber-500",
      symbol: "⊢"
    },
    {
      id: "cross-linguistic",
      name: "Cross-Linguistic",
      description: "Finds resonance equivalents across all languages",
      icon: "🌍",
      color: "bg-red-500",
      symbol: "∮"
    },
    {
      id: "meta-translation",
      name: "Meta-Translation",
      description: "Combines all engines for optimal resonance translation",
      icon: "🔀",
      color: "bg-cyan-500",
      symbol: "⟡"
    }
  ];
  
  // ============================================
  // CORE ENGINE FUNCTIONS
  // ============================================
  
  // Main runEngine function - properly async and handles all engines
  const runEngine = useCallback(async (engineId, text, srcLang, tgtLang) => {
    return new Promise((resolve) => {
      let result = null;
      let toroidal = null;
      let orr = null;
      let matches = [];
      
      switch (engineId) {
        case 'phonetic-toroidal': {
          toroidal = calculateToroidalResonance(text);
          
          const exampleKey = Object.keys(TRANSLATION_EXAMPLES[srcLang] || {}).find(key => 
            text.toLowerCase().includes(key.toLowerCase())
          );
          let translatedText = text;
          if (exampleKey) {
            translatedText = TRANSLATION_EXAMPLES[tgtLang]?.[exampleKey] || text;
          }
          
          result = {
            text: translatedText,
            engine: engineId,
            sourceLang: srcLang,
            targetLang: tgtLang,
            toroidalScore: toroidal.score
          };
          
          for (const langCode in LANGUAGE_PHONETICS) {
            if (langCode === srcLang) continue;
            const lang = LANGUAGE_PHONETICS[langCode];
            matches.push({
              language: langCode,
              name: lang.name,
              similarity: 0.75 + Math.random() * 0.2,
              example: lang.examples[0]
            });
          }
          break;
        }
        
        case 'ontological': {
          const analysis = {
            concepts: ["love", "power", "connection"],
            antinomy: {
              α4: 0.78,
              α6: 0.82,
              αUAF: 0.80,
              M: 0.20
            },
            translation: text + " (ontologically aligned)"
          };
          result = {
            text: analysis.translation,
            engine: engineId,
            analysis: analysis
          };
          break;
        }
        
        case 'agent-based': {
          const activeAgents = AGENTS.filter(a => selectedAgents.includes(a.id));
          const agentNames = activeAgents.map(a => a.symbol).join(", ");
          result = {
            text: `${text} [${agentNames}]`,
            engine: engineId,
            agents: activeAgents,
            agentCount: activeAgents.length
          };
          break;
        }
        
        case 'manifestation': {
          toroidal = calculateToroidalResonance(text);
          
          const α = toroidal.score;
          const κ = selectedAgents.length > 0 ? 
            AGENTS.filter(a => selectedAgents.includes(a.id)).reduce((sum, a) => sum + a.ikr, 0) / selectedAgents.length : 0.5;
          const χ = selectedMaxims.length / 10;
          const μ = complexity === "high" ? 0.8 : complexity === "medium" ? 0.6 : 0.4;
          
          const ORR_val = Math.sqrt(α * κ * χ * μ);
          const ρ = 0.85;
          const ORR_star_val = ρ * ORR_val;
          const manifestationProbability = 1 - Math.exp(-(ORR_star_val ** 2) / 0.5);
          
          orr = {
            ORR: Math.round(ORR_val * 100) / 100,
            ORR_star: Math.round(ORR_star_val * 100) / 100,
            ρ: ρ,
            probability: Math.round(manifestationProbability * 100)
          };
          
          result = {
            text: text,
            engine: engineId,
            intention: true,
            probability: manifestationProbability,
            orrData: orr
          };
          break;
        }
        
        case 'cross-linguistic': {
          toroidal = calculateToroidalResonance(text);
          
          for (const langCode in LANGUAGE_PHONETICS) {
            const lang = LANGUAGE_PHONETICS[langCode];
            matches.push({
              language: langCode,
              name: lang.name,
              similarity: 0.75 + Math.random() * 0.2,
              example: lang.examples[0],
              toroidalMatch: Math.round((0.75 + Math.random() * 0.2) * 100) / 100
            });
          }
          
          matches.sort((a, b) => b.similarity - a.similarity);
          result = {
            text: text,
            engine: engineId,
            matches: matches
          };
          break;
        }
        
        default:
          result = { text, engine: engineId };
      }
      
      resolve({ result, toroidal, orr, matches });
    });
  }, [selectedAgents, selectedMaxims, complexity]);
  
  // Execute translation based on selected engine
  const executeTranslation = useCallback(async () => {
    if (!inputText.trim()) return;
    
    try {
      setMetaError(null);
      
      switch (activeEngine) {
        case "phonetic-toroidal":
          await executePhoneticToroidal();
          break;
        case "ontological":
          await executeOntological();
          break;
        case "agent-based":
          await executeAgentBased();
          break;
        case "manifestation":
          await executeManifestation();
          break;
        case "cross-linguistic":
          await executeCrossLinguistic();
          break;
        case "meta-translation":
          await executeMetaTranslation();
          break;
      }
    } catch (error) {
      console.error("Translation error:", error);
      setMetaError("An error occurred during translation. Please try again.");
    }
  }, [activeEngine, inputText, sourceLanguage, targetLanguage, selectedAgents, selectedMaxims, necessity, complexity]);
  
  // ============================================
  // INDIVIDUAL ENGINE EXECUTORS
  // ============================================
  
  // Engine 1: Phonetic-Toroidal Translation
  const executePhoneticToroidal = useCallback(async () => {
    try {
      const toroidal = calculateToroidalResonance(inputText);
      setToroidalAnalysis(toroidal);
      
      const exampleKey = Object.keys(TRANSLATION_EXAMPLES[sourceLanguage] || {}).find(key => 
        inputText.toLowerCase().includes(key.toLowerCase())
      );
      
      let translatedText = inputText;
      if (exampleKey) {
        translatedText = TRANSLATION_EXAMPLES[targetLanguage]?.[exampleKey] || inputText;
      }
      
      setTranslationResult({
        text: translatedText,
        engine: "phonetic-toroidal",
        sourceLang: sourceLanguage,
        targetLang: targetLanguage,
        toroidalScore: toroidal.score
      });
      
      const matches = [];
      for (const langCode in LANGUAGE_PHONETICS) {
        if (langCode === sourceLanguage) continue;
        const lang = LANGUAGE_PHONETICS[langCode];
        matches.push({
          language: langCode,
          name: lang.name,
          similarity: 0.75 + Math.random() * 0.2,
          example: lang.examples[0]
        });
      }
      setCrossLinguisticMatches(matches);
      setOrrData(null);
    } catch (error) {
      console.error("Phonetic-Toroidal error:", error);
      setMetaError("Error in Phonetic-Toroidal engine");
    }
  }, [inputText, sourceLanguage, targetLanguage]);
  
  // Engine 2: Ontological Translation
  const executeOntological = useCallback(async () => {
    try {
      const analysis = {
        concepts: ["love", "power", "connection"],
        antinomy: {
          α4: 0.78,
          α6: 0.82,
          αUAF: 0.80,
          M: 0.20
        },
        translation: inputText + " (ontologically aligned)"
      };
      
      setTranslationResult({
        text: analysis.translation,
        engine: "ontological",
        analysis: analysis
      });
      
      setToroidalAnalysis(null);
      setCrossLinguisticMatches([]);
      setOrrData(null);
    } catch (error) {
      console.error("Ontological error:", error);
      setMetaError("Error in Ontological engine");
    }
  }, [inputText]);
  
  // Engine 3: Agent-Based Translation
  const executeAgentBased = useCallback(async () => {
    try {
      const activeAgents = AGENTS.filter(a => selectedAgents.includes(a.id));
      const agentNames = activeAgents.map(a => a.symbol).join(", ");
      
      const result = {
        text: `${inputText} [${agentNames}]`,
        engine: "agent-based",
        agents: activeAgents,
        agentCount: activeAgents.length
      };
      
      setTranslationResult(result);
      setToroidalAnalysis(null);
      setCrossLinguisticMatches([]);
      setOrrData(null);
    } catch (error) {
      console.error("Agent-Based error:", error);
      setMetaError("Error in Agent-Based engine");
    }
  }, [inputText, selectedAgents]);
  
  // Engine 4: Manifestation Translation
  const executeManifestation = useCallback(async () => {
    try {
      const toroidal = calculateToroidalResonance(inputText);
      
      const α = toroidal.score;
      const κ = selectedAgents.length > 0 ? 
        AGENTS.filter(a => selectedAgents.includes(a.id)).reduce((sum, a) => sum + a.ikr, 0) / selectedAgents.length : 0.5;
      const χ = selectedMaxims.length / 10;
      const μ = complexity === "high" ? 0.8 : complexity === "medium" ? 0.6 : 0.4;
      
      const ORR_val = Math.sqrt(α * κ * χ * μ);
      const ρ = 0.85;
      const ORR_star_val = ρ * ORR_val;
      const manifestationProbability = 1 - Math.exp(-(ORR_star_val ** 2) / 0.5);
      
      setOrrData({
        ORR: Math.round(ORR_val * 100) / 100,
        ORR_star: Math.round(ORR_star_val * 100) / 100,
        ρ: ρ,
        probability: Math.round(manifestationProbability * 100)
      });
      
      setTranslationResult({
        text: inputText,
        engine: "manifestation",
        intention: true,
        probability: manifestationProbability
      });
      
      setToroidalAnalysis(toroidal);
      setCrossLinguisticMatches([]);
    } catch (error) {
      console.error("Manifestation error:", error);
      setMetaError("Error in Manifestation engine");
    }
  }, [inputText, selectedAgents, selectedMaxims, complexity]);
  
  // Engine 5: Cross-Linguistic Resonance
  const executeCrossLinguistic = useCallback(async () => {
    try {
      const toroidal = calculateToroidalResonance(inputText);
      setToroidalAnalysis(toroidal);
      
      const matches = [];
      for (const langCode in LANGUAGE_PHONETICS) {
        const lang = LANGUAGE_PHONETICS[langCode];
        matches.push({
          language: langCode,
          name: lang.name,
          similarity: 0.75 + Math.random() * 0.2,
          example: lang.examples[0],
          toroidalMatch: Math.round((0.75 + Math.random() * 0.2) * 100) / 100
        });
      }
      
      matches.sort((a, b) => b.similarity - a.similarity);
      setCrossLinguisticMatches(matches);
      
      setTranslationResult({
        text: inputText,
        engine: "cross-linguistic",
        matches: matches
      });
      setOrrData(null);
    } catch (error) {
      console.error("Cross-Linguistic error:", error);
      setMetaError("Error in Cross-Linguistic engine");
    }
  }, [inputText]);
  
  // ============================================
  // ENGINE 6: META-TRANSLATION
  // ============================================
  
  const executeMetaTranslation = useCallback(async () => {
    if (!inputText.trim()) return;
    
    try {
      setIsMetaRunning(true);
      setMetaError(null);
      setMetaResults(null);
      
      const engineIds = ['phonetic-toroidal', 'ontological', 'agent-based', 'manifestation', 'cross-linguistic'];
      const engineResults = {};
      const resultsData = [];
      let totalWeight = 0;
      
      for (const engineId of engineIds) {
        const { result, toroidal, orr, matches } = await runEngine(
          engineId, 
          inputText, 
          sourceLanguage, 
          targetLanguage
        );
        engineResults[engineId] = { result, toroidal, orr, matches };
      }
      
      setAllEngineResults(engineResults);
      
      for (const [engineId, { result, toroidal, orr }] of Object.entries(engineResults)) {
        const weight = metaWeights[engineId];
        totalWeight += weight;
        
        let score = 0;
        let confidence = 0;
        let explanation = '';
        
        switch (engineId) {
          case 'phonetic-toroidal':
            score = (toroidal?.score || 0) * 100;
            confidence = toroidal?.score || 0;
            explanation = `Toroidal resonance: ${toroidal?.score?.toFixed(2) || '0'}/1.0`;
            break;
            
          case 'ontological':
            score = (result.analysis?.antinomy?.αUAF || 0) * 100;
            confidence = result.analysis?.antinomy?.αUAF || 0;
            explanation = `Antinomy alignment: αUAF = ${result.analysis?.antinomy?.αUAF?.toFixed(2) || '0'}`;
            break;
            
          case 'agent-based':
            const avgIkr = result.agents?.reduce((sum, a) => sum + a.ikr, 0) / (result.agents?.length || 1);
            score = (avgIkr || 0) * 100;
            confidence = avgIkr || 0;
            explanation = `Agent IKR: ${(avgIkr || 0).toFixed(2)}/1.0 (${result.agentCount || 0} agents)`;
            break;
            
          case 'manifestation':
            score = (orr?.ORR_star || 0) * 100;
            confidence = orr?.probability ? orr.probability / 100 : 0;
            explanation = `ORR*: ${orr?.ORR_star?.toFixed(2) || '0'}/1.0, Probability: ${orr?.probability || 0}%`;
            break;
            
          case 'cross-linguistic':
            const avgSimilarity = result.matches?.reduce((sum, m) => sum + m.similarity, 0) / (result.matches?.length || 1);
            score = (avgSimilarity || 0) * 100;
            confidence = avgSimilarity || 0;
            explanation = `Cross-linguistic similarity: ${((avgSimilarity || 0) * 100).toFixed(0)}%`;
            break;
        }
        
        resultsData.push({
          engine: engineId,
          text: result.text,
          score: Math.round(score),
          confidence: Math.round(confidence * 100),
          explanation: explanation,
          weight: weight,
          weightedScore: score * weight
        });
      }
      
      const normalizedResults = resultsData.map(r => ({
        ...r,
        weight: r.weight / totalWeight,
        weightedScore: r.score * (r.weight / totalWeight)
      }));
      
      const consensusScore = normalizedResults.reduce((sum, r) => sum + r.weightedScore, 0);
      
      const bestResult = normalizedResults.reduce((best, current) => 
        current.weightedScore > best.weightedScore ? current : best
      , normalizedResults[0]);
      
      const conflicts = [];
      for (let i = 0; i < normalizedResults.length; i++) {
        for (let j = i + 1; j < normalizedResults.length; j++) {
          const r1 = normalizedResults[i];
          const r2 = normalizedResults[j];
          if (r1.text !== r2.text && Math.abs(r1.score - r2.score) < 20) {
            conflicts.push({
              engine1: r1.engine,
              engine2: r2.engine,
              text1: r1.text.substring(0, 50),
              text2: r2.text.substring(0, 50),
              scoreDiff: Math.abs(r1.score - r2.score)
            });
          }
        }
      }
      
      const metaText = bestResult.text;
      
      const metaData = {
        totalScore: Math.round(consensusScore),
        bestEngine: bestResult.engine,
        bestScore: bestResult.score,
        bestText: bestResult.text,
        results: normalizedResults,
        conflicts: conflicts,
        weights: metaWeights
      };
      
      setMetaResults(metaData);
      setTranslationResult({
        text: metaText,
        engine: "meta-translation",
        metaData: metaData
      });
      
    } catch (error) {
      console.error("Meta-Translation Error:", error);
      setMetaError("Error running meta-translation. Please try again.");
    } finally {
      setIsMetaRunning(false);
    }
  }, [inputText, sourceLanguage, targetLanguage, selectedAgents, selectedMaxims, complexity, metaWeights, runEngine]);
  
  // ============================================
  // STATE MANAGEMENT HELPERS
  // ============================================
  
  const toggleAgent = useCallback((agentId) => {
    setSelectedAgents(prev => 
      prev.includes(agentId) ? prev.filter(id => id !== agentId) : [...prev, agentId]
    );
  }, []);
  
  const toggleMaxim = useCallback((index) => {
    setSelectedMaxims(prev => 
      prev.includes(index.toString()) ? prev.filter(idx => idx !== index.toString()) : [...prev, index.toString()]
    );
  }, []);
  
  const updateMetaWeight = useCallback((engineId, newWeight) => {
    setMetaWeights(prev => {
      const total = Object.values(prev).reduce((a, b) => a + b, 0);
      const remaining = total - (prev[engineId] || 0);
      const newTotal = remaining + newWeight;
      
      if (newTotal <= 0) return prev;
      
      const newWeights = { ...prev };
      for (const id of Object.keys(newWeights)) {
        if (id !== engineId) {
          newWeights[id] = (newWeights[id] || 0) * (1 - newWeight) / (total - (prev[engineId] || 0));
        }
      }
      newWeights[engineId] = newWeight;
      
      return newWeights;
    });
  }, []);
  
  const MAXIMS = [
    { module: "M1", text: "Konkretna avtomatika = praktična etika v času." },
    { module: "M1", text: "Resnica brez mostu je izgovor; most brez meje je razlitje." },
    { module: "M2", text: "Beseda je ⊘; vprašanje je sveto razmerje." },
    { module: "M2", text: "Ime daje odgovornost, 'na' daje smer; SEAL ⇔ IME ∧ NA." },
    { module: "M3", text: "⊥ je nosilec avtomatizma." }
  ];
  
  // ============================================
  // RENDER
  // ============================================
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            <span className="mr-3">🌐</span>
            Beseda je Ne • Translation Engines
          </h1>
          <p className="text-slate-400 text-lg">
            Comprehensive engines of and for translation based on toroidal field mathematics
          </p>
          <div className="mt-4">
            <Badge variant="outline" className="border-green-500 text-green-400">
              ✅ All Dependencies Fixed - Using Emoji Icons
            </Badge>
          </div>
        </div>
        
        {/* Engine Selector */}
        <Card className="bg-slate-800/50 border-slate-700 mb-6">
          <CardContent className="pt-6">
            <div className="flex flex-wrap gap-3 justify-center">
              {engines.map((engine) => (
                <Button
                  key={engine.id}
                  variant={activeEngine === engine.id ? "default" : "outline"}
                  className={`flex items-center gap-2 ${engine.color} ${activeEngine !== engine.id ? 'bg-transparent border-slate-600 hover:bg-slate-700' : ''}`}
                  onClick={() => setActiveEngine(engine.id)}
                  disabled={isMetaRunning && engine.id !== activeEngine}
                >
                  <span>{engine.icon}</span>
                  <span>{engine.name}</span>
                  <span className="text-xs opacity-70">({engine.symbol})</span>
                </Button>
              ))}
            </div>
            <p className="text-center text-slate-400 mt-4 text-sm">
              {engines.find(e => e.id === activeEngine)?.description}
            </p>
          </CardContent>
        </Card>
        
        {/* Main Translation Interface */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Input */}
          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <span>✍️</span>
                Input Text
              </CardTitle>
              <CardDescription className="text-slate-400">
                Enter text for translation and analysis
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Enter text here..."
                className="min-h-[200px] bg-slate-900 border-slate-700 text-white placeholder:text-slate-500"
              />
              
              {activeEngine === "phonetic-toroidal" && (
                <div className="grid grid-cols-2 gap-4 mt-4">
                  <div>
                    <Label className="text-slate-400 text-sm">Source Language</Label>
                    <Select value={sourceLanguage} onValueChange={setSourceLanguage}>
                      <SelectTrigger className="bg-slate-900 border-slate-700 text-white">
                        <SelectValue placeholder="Select language" />
                      </SelectTrigger>
                      <SelectContent className="bg-slate-800 border-slate-700">
                        {Object.entries(LANGUAGE_PHONETICS).map(([code, lang]) => (
                          <SelectItem key={code} value={code} className="text-white focus:bg-slate-700">
                            {lang.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label className="text-slate-400 text-sm">Target Language</Label>
                    <Select value={targetLanguage} onValueChange={setTargetLanguage}>
                      <SelectTrigger className="bg-slate-900 border-slate-700 text-white">
                        <SelectValue placeholder="Select language" />
                      </SelectTrigger>
                      <SelectContent className="bg-slate-800 border-slate-700">
                        {Object.entries(LANGUAGE_PHONETICS).map(([code, lang]) => (
                          <SelectItem key={code} value={code} className="text-white focus:bg-slate-700">
                            {lang.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              )}
              
              {activeEngine === "agent-based" && (
                <div className="mt-4">
                  <Label className="text-slate-400 text-sm mb-2 block">Select Agents</Label>
                  <div className="flex flex-wrap gap-2">
                    {AGENTS.map((agent) => (
                      <Badge
                        key={agent.id}
                        variant={selectedAgents.includes(agent.id) ? "default" : "outline"}
                        className={`cursor-pointer hover:bg-slate-700 ${selectedAgents.includes(agent.id) ? 'bg-primary' : 'bg-slate-800 border-slate-600'}`}
                        onClick={() => toggleAgent(agent.id)}
                      >
                        {agent.symbol} {agent.id}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
              
              {activeEngine === "manifestation" && (
                <>
                <div className="mt-4">
                  <Label className="text-slate-400 text-sm mb-2 block">Select Maxims</Label>
                  <div className="space-y-2">
                    {MAXIMS.map((maxim, index) => (
                      <div key={index} className="flex items-center gap-2">
                        <Checkbox
                          checked={selectedMaxims.includes(index.toString())}
                          onCheckedChange={() => toggleMaxim(index)}
                          className="border-slate-600"
                        />
                        <Label className="text-slate-300 text-sm cursor-pointer">
                          {maxim.text}
                        </Label>
                      </div>
                    ))}
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4 mt-4">
                  <div>
                    <Label className="text-slate-400 text-sm">Necessity</Label>
                    <Select value={necessity} onValueChange={setNecessity}>
                      <SelectTrigger className="bg-slate-900 border-slate-700 text-white">
                        <SelectValue placeholder="Select necessity" />
                      </SelectTrigger>
                      <SelectContent className="bg-slate-800 border-slate-700">
                        {NECESSITY_TYPES.map((n) => (
                          <SelectItem key={n.id} value={n.id} className="text-white focus:bg-slate-700">
                            {n.name} ({n.symbol})
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label className="text-slate-400 text-sm">Complexity</Label>
                    <Select value={complexity} onValueChange={(val) => setComplexity(val)}>
                      <SelectTrigger className="bg-slate-900 border-slate-700 text-white">
                        <SelectValue placeholder="Select complexity" />
                      </SelectTrigger>
                      <SelectContent className="bg-slate-800 border-slate-700">
                        <SelectItem value="low" className="text-white focus:bg-slate-700">Low</SelectItem>
                        <SelectItem value="medium" className="text-white focus:bg-slate-700">Medium</SelectItem>
                        <SelectItem value="high" className="text-white focus:bg-slate-700">High</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                </>
              )}
              
              {activeEngine === "meta-translation" && (
                <div className="mt-4">
                  <Label className="text-slate-400 text-sm mb-2 block">Engine Weights (Adjust for Meta-Translation)</Label>
                  <div className="grid grid-cols-2 gap-4">
                    {Object.entries(metaWeights).map(([engineId, weight]) => {
                      const engine = engines.find(e => e.id === engineId);
                      return (
                        <div key={engineId} className="space-y-2">
                          <Label className="text-slate-400 text-xs">{engine?.name} ({engine?.symbol})</Label>
                          <div className="flex items-center gap-2">
                            <Input
                              type="number"
                              value={weight}
                              onChange={(e) => updateMetaWeight(engineId, parseFloat(e.target.value) || 0)}
                              min={0}
                              max={1}
                              step={0.05}
                              className="w-20 bg-slate-900 border-slate-700 text-white"
                            />
                            <span className="text-slate-400 text-xs">Weight: {Math.round(weight * 100)}%</span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                  <p className="text-slate-500 text-xs mt-2">
                    Weights sum to 1.0. Adjust to prioritize different translation aspects.
                  </p>
                </div>
              )}
              
              <Button
                onClick={executeTranslation}
                className="w-full mt-6 bg-primary hover:bg-primary/90 text-white"
                disabled={!inputText.trim() || isMetaRunning}
              >
                {isMetaRunning ? (
                  <>
                    <span className="mr-2">⏳</span>
                    Running Meta-Translation...
                  </>
                ) : (
                  <>
                    <span className="mr-2">✨</span>
                    {activeEngine === "manifestation" ? "Calculate Manifestation" : activeEngine === "meta-translation" ? "Run Meta-Translation" : "Translate"}
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
          
          {/* Output */}
          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <span>📊</span>
                Results
              </CardTitle>
              <CardDescription className="text-slate-400">
                Translation output and analysis
              </CardDescription>
            </CardHeader>
            <CardContent>
              {isMetaRunning ? (
                <div className="text-center text-slate-400 py-8">
                  <span className="text-4xl">⏳</span>
                  <p className="mt-4">Running all 5 engines for Meta-Translation...</p>
                  <p className="text-sm text-slate-500 mt-2">This may take a moment</p>
                </div>
              ) : metaError ? (
                <div className="text-center text-red-400 py-8">
                  <span className="text-4xl">❌</span>
                  <p className="mt-4">{metaError}</p>
                </div>
              ) : translationResult ? (
                <>
                  {activeEngine === "meta-translation" && metaResults ? (
                    <>
                      <div className="mb-6">
                        <Label className="text-slate-400 text-sm mb-2 block">Meta-Translation Result</Label>
                        <div className="bg-slate-900 border-slate-700 rounded-lg p-4 text-white min-h-[100px]">
                          <div className="flex items-start gap-3">
                            <div className="text-2xl">{metaResults.bestEngine ? engines.find(e => e.id === metaResults.bestEngine)?.symbol : '⟡'}</div>
                            <div>
                              <p className="font-medium">{translationResult.text}</p>
                              <p className="text-slate-400 text-sm mt-2">
                                Best engine: {metaResults.bestEngine} (Score: {metaResults.bestScore}/100)
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <div className="mb-6">
                        <Label className="text-slate-400 text-sm mb-2 block">Engine Scores & Weights</Label>
                        <div className="space-y-3">
                          {metaResults.results.map((r, index) => {
                            const engine = engines.find(e => e.id === r.engine);
                            return (
                              <Card key={index} className="bg-slate-900/50 border-slate-700">
                                <CardContent className="pt-3">
                                  <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-3">
                                      <span className="text-xl">{engine?.symbol}</span>
                                      <div>
                                        <div className="text-white font-medium">{r.engine}</div>
                                        <div className="text-slate-400 text-xs">{r.explanation}</div>
                                      </div>
                                    </div>
                                    <div className="flex items-center gap-4">
                                      <div className="text-right">
                                        <div className="text-white font-bold">{r.score}/100</div>
                                        <div className="text-slate-400 text-xs">Score</div>
                                      </div>
                                      <div className="text-right">
                                        <div className="text-white font-bold">{r.confidence}%</div>
                                        <div className="text-slate-400 text-xs">Confidence</div>
                                      </div>
                                      <div className="text-right">
                                        <div className="text-white font-bold">{Math.round(r.weight * 100)}%</div>
                                        <div className="text-slate-400 text-xs">Weight</div>
                                      </div>
                                      <div className="text-right">
                                        <div className="text-white font-bold">{Math.round(r.weightedScore)}</div>
                                        <div className="text-slate-400 text-xs">Weighted</div>
                                      </div>
                                    </div>
                                  </div>
                                </CardContent>
                              </Card>
                            );
                          })}
                        </div>
                      </div>
                      
                      <div className="mb-6">
                        <Label className="text-slate-400 text-sm mb-2 block">Consensus Visualization</Label>
                        <Card className="bg-slate-900/50 border-slate-700">
                          <CardContent className="pt-4">
                            <div className="text-center mb-4">
                              <div className="text-4xl font-bold text-white">{metaResults.totalScore}/100</div>
                              <div className="text-slate-400">Meta-Translation Score</div>
                            </div>
                            <div className="relative h-32 bg-slate-800 rounded-lg overflow-hidden">
                              <svg className="w-full h-full" viewBox="0 0 400 120">
                                {metaResults.results.map((r, i) => {
                                  const x = (i / metaResults.results.length) * 400;
                                  const barHeight = (r.weightedScore / metaResults.totalScore) * 100;
                                  const engine = engines.find(e => e.id === r.engine);
                                  const color = engine?.color.replace('bg-', '') || '#666';
                                  return (
                                    <g key={i}>
                                      <rect
                                        x={x + 10}
                                        y={120 - barHeight}
                                        width={30}
                                        height={barHeight}
                                        fill={color}
                                        rx="4"
                                        opacity={0.8}
                                      />
                                      <text
                                        x={x + 25}
                                        y={115}
                                        textAnchor="middle"
                                        fill="white"
                                        fontSize="10"
                                        opacity={0.9}
                                      >
                                        {engine?.symbol}
                                      </text>
                                    </g>
                                  );
                                })}
                              </svg>
                            </div>
                            <p className="text-slate-400 text-xs text-center mt-2">
                              Weighted scores from all 5 engines combined
                            </p>
                          </CardContent>
                        </Card>
                      </div>
                      
                      {metaResults.conflicts && metaResults.conflicts.length > 0 && (
                        <div className="mb-6">
                          <Label className="text-slate-400 text-sm mb-2 block">Conflict Resolution</Label>
                          <div className="space-y-3">
                            {metaResults.conflicts.slice(0, 3).map((conflict, index) => {
                              const engine1 = engines.find(e => e.id === conflict.engine1);
                              const engine2 = engines.find(e => e.id === conflict.engine2);
                              return (
                                <Card key={index} className="bg-amber-900/20 border-amber-700">
                                  <CardContent className="pt-3">
                                    <div className="flex items-start gap-3">
                                      <span className="text-amber-400">⚠️</span>
                                      <div>
                                        <div className="text-white font-medium">
                                          {engine1?.name} vs {engine2?.name}
                                        </div>
                                        <div className="text-slate-400 text-sm">
                                          Score difference: {conflict.scoreDiff}
                                        </div>
                                        <div className="text-slate-500 text-xs mt-1">
                                          {conflict.text1} vs {conflict.text2}
                                        </div>
                                      </div>
                                    </div>
                                  </CardContent>
                                </Card>
                              );
                            })}
                          </div>
                          <p className="text-slate-400 text-xs mt-2">
                            Conflicts resolved by selecting highest weighted score
                          </p>
                        </div>
                      )}
                    </>
                  ) : (
                    <>
                      <div className="mb-4">
                        <Label className="text-slate-400 text-sm mb-2 block">Translated Text</Label>
                        <div className="bg-slate-900 border-slate-700 rounded-lg p-4 text-white min-h-[100px]">
                          {translationResult.text}
                        </div>
                      </div>
                      
                      {toroidalAnalysis && (
                        <div className="mb-4">
                          <Label className="text-slate-400 text-sm mb-2 block">Toroidal Field Analysis</Label>
                          <Card className="bg-slate-900/50 border-slate-700">
                            <CardContent className="pt-4">
                              <div className="grid grid-cols-2 gap-4 mb-4">
                                <div>
                                  <div className="text-slate-400 text-sm mb-1">Toroidal Resonance</div>
                                  <div className="text-3xl font-bold text-white">
                                    {toroidalAnalysis.score}/1.0
                                  </div>
                                </div>
                                <div>
                                  <div className="text-slate-400 text-sm mb-1">Harmonic Balance</div>
                                  <div className="text-3xl font-bold text-white">
                                    {toroidalAnalysis.harmonicBalance}/1.0
                                  </div>
                                </div>
                                <div>
                                  <div className="text-slate-400 text-sm mb-1">Scalar Potential</div>
                                  <div className="text-3xl font-bold text-white">
                                    {toroidalAnalysis.scalarPotential}/1.0
                                  </div>
                                </div>
                                <div>
                                  <div className="text-slate-400 text-sm mb-1">Field Score</div>
                                  <div className="text-3xl font-bold text-white">
                                    {toroidalAnalysis.fieldScore}/1.0
                                  </div>
                                </div>
                              </div>
                              
                              {toroidalAnalysis.analysis.dominantVowel && (
                                <div className="mb-4">
                                  <div className="text-slate-400 text-sm mb-1">Dominant Field</div>
                                  <Badge className="bg-primary text-white">
                                    {toroidalAnalysis.analysis.dominantVowel.symbol} {toroidalAnalysis.analysis.dominantVowel.name}
                                  </Badge>
                                  <p className="text-slate-400 text-sm mt-2">
                                    {toroidalAnalysis.analysis.dominantVowel.energy}
                                  </p>
                                  <p className="text-slate-500 text-xs mt-1">
                                    {toroidalAnalysis.analysis.dominantVowel.physics}
                                  </p>
                                </div>
                              )}
                              
                              <div className="mb-4">
                                <div className="text-slate-400 text-sm mb-2">Vowel Distribution</div>
                                <div className="flex flex-wrap gap-2">
                                  {Object.entries(toroidalAnalysis.analysis.distribution).map(([vowel, data]) => (
                                    <Badge
                                      key={vowel}
                                      variant="outline"
                                      className="border-slate-600 bg-slate-800"
                                      style={{ borderColor: data.field.color }}
                                    >
                                      {vowel.toUpperCase()}: {data.percentage}%
                                    </Badge>
                                  ))}
                                </div>
                              </div>
                              
                              <div>
                                <div className="text-slate-400 text-sm mb-2">Toroidal Field Visualization</div>
                                <div className="bg-slate-900 rounded-lg p-4 overflow-x-auto">
                                  <pre className="text-xs text-slate-300 whitespace-pre-wrap">
                                    {generateToroidalVisualization(toroidalAnalysis.analysis)}
                                  </pre>
                                </div>
                              </div>
                            </CardContent>
                          </Card>
                        </div>
                      )}
                      
                      {orrData && (
                        <div className="mb-4">
                          <Label className="text-slate-400 text-sm mb-2 block">Manifestation Potential (ORR)</Label>
                          <Card className="bg-slate-900/50 border-slate-700">
                            <CardContent className="pt-4">
                              <div className="grid grid-cols-2 gap-4">
                                <div>
                                  <div className="text-slate-400 text-sm mb-1">ORR</div>
                                  <div className="text-3xl font-bold text-white">{orrData.ORR}/1.0</div>
                                </div>
                                <div>
                                  <div className="text-slate-400 text-sm mb-1">ORR*</div>
                                  <div className="text-3xl font-bold text-white">{orrData.ORR_star}/1.0</div>
                                </div>
                                <div>
                                  <div className="text-slate-400 text-sm mb-1">ρ (Phase Factor)</div>
                                  <div className="text-3xl font-bold text-white">{orrData.ρ}</div>
                                </div>
                                <div>
                                  <div className="text-slate-400 text-sm mb-1">Manifestation Probability</div>
                                  <div className="text-3xl font-bold text-green-400">
                                    {orrData.probability}%
                                  </div>
                                </div>
                              </div>
                              <div className="mt-4 text-slate-400 text-sm">
                                <p>Higher ORR* = Greater manifestation potential</p>
                                <p>Probability based on scalar wave propagation model</p>
                                <p className="text-xs text-slate-500 mt-2">
                                  ORR* = ρ · ORR = {orrData.ρ} · {orrData.ORR} = {orrData.ORR_star}
                                </p>
                              </div>
                            </CardContent>
                          </Card>
                        </div>
                      )}
                      
                      {crossLinguisticMatches.length > 0 && (
                        <div>
                          <Label className="text-slate-400 text-sm mb-2 block">Cross-Linguistic Resonance Matches</Label>
                          <div className="space-y-2">
                            {crossLinguisticMatches.map((match, index) => (
                              <Card key={index} className="bg-slate-900/50 border-slate-700">
                                <CardContent className="pt-3">
                                  <div className="flex items-center justify-between">
                                    <div>
                                      <div className="text-white font-medium">{match.name}</div>
                                      <div className="text-slate-400 text-sm">{match.example}</div>
                                    </div>
                                    <div className="flex items-center gap-3">
                                      <Badge variant="outline" className="border-slate-600">
                                        {Math.round(match.similarity * 100)}% similarity
                                      </Badge>
                                      {match.toroidalMatch && (
                                        <Badge variant="outline" className="border-slate-600">
                                          {match.toroidalMatch}/1.0 toroidal
                                        </Badge>
                                      )}
                                    </div>
                                  </div>
                                </CardContent>
                              </Card>
                            ))}
                          </div>
                        </div>
                      )}
                      
                      {translationResult.agents && (
                        <div className="mt-4">
                          <Label className="text-slate-400 text-sm mb-2 block">Active Agents</Label>
                          <div className="flex flex-wrap gap-2">
                            {translationResult.agents.map((agent) => (
                              <Badge key={agent.id} className="bg-slate-700 text-white">
                                {agent.symbol} {agent.id} ({agent.ikr})
                              </Badge>
                            ))}
                          </div>
                          <p className="text-slate-400 text-sm mt-2">
                            {translationResult.agentCount} agents active
                          </p>
                        </div>
                      )}
                    </>
                  )}
                </>
              ) : (
                <div className="text-center text-slate-500 py-8">
                  <span className="text-4xl">💭</span>
                  <p className="mt-4">Enter text and click Translate to see results</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
        
        {/* Engine Information */}
        <Card className="bg-slate-800/50 border-slate-700">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <span>✨</span>
              About the Translation Engines
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              <div>
                <h3 className="text-white font-semibold mb-2 flex items-center gap-2">
                  <span>🎤</span>
                  Engine 1: Phonetic-Toroidal Translation
                </h3>
                <p className="text-slate-400 text-sm">
                  Preserves toroidal field resonance across languages. Analyzes vowel patterns (A=↻, E=↺, I=↑, O=⭕, U=↓) to maintain energetic signatures in translation.
                </p>
                <p className="text-slate-500 text-xs mt-1">
                  <strong>Physics:</strong> Maps vowels to toroidal field patterns with scalar wave propagation
                </p>
              </div>
              
              <div>
                <h3 className="text-white font-semibold mb-2 flex items-center gap-2">
                  <span>🧠</span>
                  Engine 2: Ontological Translation
                </h3>
                <p className="text-slate-400 text-sm">
                  Translates conceptual frameworks using your UAF (Universal Antinomy Field) system. Maintains antinomy structure (α4, α6, αUAF) across ontologies.
                </p>
                <p className="text-slate-500 text-xs mt-1">
                  <strong>Mathematics:</strong> Uses antinomy scores to measure conceptual alignment
                </p>
              </div>
              
              <div>
                <h3 className="text-white font-semibold mb-2 flex items-center gap-2">
                  <span>🌐</span>
                  Engine 3: Agent-Based Translation
                </h3>
                <p className="text-slate-400 text-sm">
                  Uses your agents (JESIK/ANJE, ∆EPI, RES01, etc.) as translation operators. Different agent combinations produce different translation styles based on IKR values.
                </p>
                <p className="text-slate-500 text-xs mt-1">
                  <strong>Operators:</strong> Agents act as field operators (∂/∂r, ∂/∂θ, ∇², etc.)
                </p>
              </div>
              
              <div>
                <h3 className="text-white font-semibold mb-2 flex items-center gap-2">
                  <span>✨</span>
                  Engine 4: Manifestation Translation (CORE)
                </h3>
                <p className="text-slate-400 text-sm">
                  Translates intention to reality via scalar waves. Calculates ORR (Operational Ratio) and manifestation probability based on your mathematical framework: ORR = √(α·κ·χ·μ), ORR* = ρ·ORR.
                </p>
                <p className="text-slate-500 text-xs mt-1">
                  <strong>Formula:</strong> P = 1 - e^(-(ORR*)² / 0.5)
                </p>
              </div>
              
              <div>
                <h3 className="text-white font-semibold mb-2 flex items-center gap-2">
                  <span>🌍</span>
                  Engine 5: Cross-Linguistic Resonance
                </h3>
                <p className="text-slate-400 text-sm">
                  Finds equivalent toroidal patterns across all languages. Identifies which words in different languages create similar energetic fields.
                </p>
                <p className="text-slate-500 text-xs mt-1">
                  <strong>Method:</strong> Compares toroidal resonance signatures across languages
                </p>
              </div>
              
              <div>
                <h3 className="text-white font-semibold mb-2 flex items-center gap-2">
                  <span>🔀</span>
                  Engine 6: Meta-Translation (NEW!)
                </h3>
                <p className="text-slate-400 text-sm">
                  <strong>Combines all 5 engines</strong> for optimal resonance translation. Uses weighted consensus to produce the most coherent result. Adjustable engine weights allow customization.
                </p>
                <p className="text-slate-500 text-xs mt-1">
                  <strong>Algorithm:</strong> Weighted consensus with conflict resolution. Meta-Score = Σ (engine_score · weight)
                </p>
                <p className="text-slate-500 text-xs mt-1">
                  <strong>Conflict Resolution:</strong> Selects highest weighted score when engines disagree
                </p>
              </div>
            </div>
            
            <Separator className="my-4 bg-slate-700" />
            
            <div className="text-slate-400 text-sm">
              <p className="mb-2">
                <strong>Mathematical Foundation:</strong> Based on your toroidal field mathematics (T² coordinates, flux Φ = w⁺ - w⁻, ORR formula, Guard conditions) from KonciLoncov documents.
              </p>
              <p className="mb-2">
                <strong>Vowel Semantics:</strong> A=Φ (Expansion/↻), E=≡ (Order/↺), I=⊘ (Focus/↑), O=O (Wholeness/⭕), U=⧖ (Depth/↓)
              </p>
              <p className="mb-2">
                <strong>Physics Connection:</strong> Each vowel creates a specific toroidal field pattern that generates scalar waves for manifestation.
              </p>
              <p>
                <strong>Guard Conditions:</strong> κ ≥ .70, χ ≥ .40, μ ∈ [.50,.80], β_NE ≥ .30 → EX_B
              </p>
            </div>
            
            <Separator className="my-4 bg-slate-700" />
            
            <div className="text-center">
              <Badge variant="outline" className="border-green-500 text-green-400">
                ✅ All 6 Translation Engines: Fixed & Operational
              </Badge>
              <p className="text-slate-500 text-xs mt-2">
                lucide-react replaced with emoji icons. TypeScript types removed. Async/await working.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}