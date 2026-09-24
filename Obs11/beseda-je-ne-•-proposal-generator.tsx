import React, { useState, useMemo, useCallback } from "react";
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Textarea } from "@/components/ui/textarea";
import { Separator } from "@/components/ui/separator";
import { Checkbox } from "@/components/ui/checkbox";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogDescription } from "@/components/ui/dialog";
import { Plus, X, Sparkles, Target, Layers, FileText, Brain, Zap, Upload, Download, Link2, Eye, BarChart3 } from "lucide-react";

// ============================================
// DATA - Now with CSV parsing support
// ============================================

// Initial mock data - will be replaced by CSV imports
let AGENTS = [
  { id: "JESIK/ANJE", symbol: "∆J", function: "strike_inert_thought", ikr: 0.75, category: "Cognitive" },
  { id: "∆EPI", symbol: "∆↻", function: "close_cycle_no_censor", ikr: 0.6, category: "Cognitive" },
  { id: "RES01", symbol: "∮≠→1", function: "measure_truth_distance", ikr: 0.8, category: "Measurement" },
  { id: "LAŽ¬", symbol: "¬≠", function: "negation_carrier", ikr: 0.9, category: "Logical" },
  { id: "BOL·LOB", symbol: "≠∫", function: "transform_wound", ikr: 0.7, category: "Transformation" },
  { id: "∆HALO", symbol: "∆H⟡", function: "excuse_vs_call_test", ikr: 0.78, category: "Testing" },
  { id: "∅MOLK", symbol: "∅∆", function: "absorb_sound", ikr: 0.0, category: "Somatic" },
  { id: "∆GLAS", symbol: "⟡↑", function: "JEWIK_sound_filter", ikr: 0.78, category: "Audio" },
  { id: "O≡0", symbol: "O≡0", function: "field_of_presence", ikr: 0.5, category: "Cosmic" },
  { id: "∮TIME", symbol: "∮∞", function: "breath_1↔∞", ikr: 0.85, category: "Temporal" },
];

let MAXIMS = [
  { module: "M1 · OSNOVNE", text: "Konkretna avtomatika = praktična etika v času." },
  { module: "M1 · OSNOVNE", text: "Resnica brez mostu je izgovor; most brez meje je razlitje." },
  { module: "M1 · OSNOVNE", text: "Ljubezen brez resničnega pogleda je fata morgana: greje, zaslepi, ožge — dokler rez (⊘) ne postane most (∴) za premik (∆)." },
  { module: "M2 · JEZIK", text: "Beseda je ⊘; vprašanje je sveto razmerje." },
  { module: "M2 · JEZIK", text: "Ime daje odgovornost, 'na' daje smer; SEAL ⇔ IME ∧ NA." },
  { module: "M3 · TELO", text: "⊥ je nosilec avtomatizma." },
  { module: "M3 · TELO", text: "Dih uravnava μ; stabilen ritem zniža ℜ." },
  { module: "M4 · ČAS", text: "⧖ je utrip prehodov; brez cikla ni SEAL." },
];

// Necessity types
const NECESSITY_TYPES = [
  { id: "stability", name: "Stability", symbol: "⊥", description: "System requires grounding", weight: 0.2 },
  { id: "contradiction", name: "Contradiction", symbol: "⊘", description: "Opposing forces need resolution", weight: 0.3 },
  { id: "energy", name: "Energy", symbol: "∆", description: "Action or transformation needed", weight: 0.25 },
  { id: "pattern", name: "Pattern", symbol: "∮", description: "Repetition or cycle detection", weight: 0.2 },
  { id: "boundary", name: "Boundary", symbol: "∴", description: "Limits or constraints required", weight: 0.25 },
];

// Existing proposals from library with enhanced data
const EXISTING_PROPOSALS = [
  { id: "P1", title: "Unified Operator Registry", description: "Merge SKILL.md §8, 92 nujnosti, Tihinska glyphs", status: "Draft", score: 0.4, tags: ["registry", "symbols", "unification"], dependencies: [] },
  { id: "P2", title: "Tihinska Agent Integration", description: "Add 6+ Tihinska agents to taxonomy", status: "Draft", score: 0.3, tags: ["agents", "tihinska", "integration"], dependencies: ["P1"] },
  { id: "P3", title: "Development Timeline", description: "Map 46 notes chronologically", status: "Draft", score: 0.5, tags: ["timeline", "history", "tracking"], dependencies: [] },
  { id: "P4", title: "Gap Analysis", description: "Identify missing connections", status: "In Progress", score: 0.7, tags: ["analysis", "gaps", "connections"], dependencies: ["P1", "P3"] },
  { id: "P5", title: "Canonical Document Set", description: "11 document specs with cross-references", status: "Draft", score: 0.6, tags: ["documents", "canonical", "formalization"], dependencies: ["P1"] },
  { id: "P6", title: "MAXIME ↔ SKILL.md Mapping", description: "8 rules ↔ 96 maxims", status: "Draft", score: 0.8, tags: ["mapping", "maxims", "skill"], dependencies: [] },
  { id: "P7", title: "F(x) ↔ Ψ(x) Integration", description: "Composed formula F_Ψ(x)", status: "Draft", score: 0.5, tags: ["formula", "integration", "consciousness"], dependencies: ["P4"] },
  { id: "P8", title: "AMR ↔ F(x) Formal Mapping", description: "Proof that AMR ⊂ F(x)", status: "Draft", score: 0.6, tags: ["proof", "mapping", "formal"], dependencies: ["P7"] },
  { id: "P9", title: "Concept Genealogy", description: "Dependency graph with ne=1/0 as root", status: "Draft", score: 0.4, tags: ["genealogy", "concepts", "graph"], dependencies: ["P3"] },
];

// ============================================
// CSV PARSING UTILITIES
// ============================================

// Parse CSV text into array of objects
const parseCSV = (csvText, delimiter = ",") => {
  const lines = csvText.split("\n");
  if (lines.length < 2) return [];
  
  const headers = lines[0].split(delimiter).map(h => h.trim());
  const data = [];
  
  for (let i = 1; i < lines.length; i++) {
    if (!lines[i].trim()) continue;
    const values = lines[i].split(delimiter);
    const entry = {};
    headers.forEach((header, index) => {
      entry[header] = values[index] ? values[index].trim() : "";
    });
    data.push(entry);
  }
  
  return data;
};

// Parse agents CSV
const parseAgentsCSV = (csvText) => {
  const data = parseCSV(csvText);
  return data.map(row => ({
    id: row.id || row.Beseda || "",
    symbol: row.symbol || row.Simbol || "",
    function: row.function || row.Funkcija || row.Funkcija || "",
    ikr: parseFloat(row.ikr || row.ikrw || row.IKR || 0),
    category: row.category || row.Ontologija || "Unknown"
  })).filter(a => a.id);
};

// Parse maxims CSV
const parseMaximsCSV = (csvText) => {
  const data = parseCSV(csvText);
  return data.map(row => ({
    module: row.module || row.Module || "",
    text: row.text || row.Text || row.maxim || row.Maxim || ""
  })).filter(m => m.text);
};

// ============================================
// PROPOSAL GENERATION LOGIC
// ============================================

// Generate a unique ID
const generateId = () => {
  return "PROP-" + Date.now().toString(36).toUpperCase() + "-" + Math.random().toString(36).substring(2, 6).toUpperCase();
};

// Advanced scoring with multiple factors
const calculateScore = (proposal) => {
  let score = 0;
  const weights = { agent: 0.35, maxim: 0.25, necessity: 0.2, complexity: 0.1, dependency: 0.1 };
  
  // Agent coverage (0-0.35)
  if (proposal.agents && proposal.agents.length > 0) {
    const avgIkr = proposal.agents.reduce((sum, a) => sum + (a.ikr || 0), 0) / proposal.agents.length;
    const countScore = Math.min(proposal.agents.length / 10, 1); // Normalize to 0-1
    score += (avgIkr * 0.6 + countScore * 0.4) * weights.agent;
  }
  
  // Maxim alignment (0-0.25)
  if (proposal.maxims && proposal.maxims.length > 0) {
    const maximScore = Math.min(proposal.maxims.length / 5, 1);
    score += maximScore * weights.maxim;
  }
  
  // Necessity urgency (0-0.2)
  if (proposal.necessity) {
    const necessity = NECESSITY_TYPES.find(n => n.id === proposal.necessity);
    if (necessity) {
      score += necessity.weight * weights.necessity;
    }
  }
  
  // Complexity bonus (0-0.1)
  if (proposal.complexity === "high") {
    score += 0.1 * weights.complexity;
  } else if (proposal.complexity === "medium") {
    score += 0.05 * weights.complexity;
  }
  
  // Dependency penalty/reward (0-0.1)
  if (proposal.dependencies && proposal.dependencies.length > 0) {
    // Reward for linking to existing proposals
    score += Math.min(proposal.dependencies.length * 0.05, 0.1) * weights.dependency;
  }
  
  return Math.round(score * 100) / 100;
};

// Generate proposal text
const generateProposalText = (proposal) => {
  const lines = [
    `## ${proposal.title}`,
    ``,
    `**ID:** ${proposal.id}`,
    `**Type:** ${proposal.type}`,
    `**Necessity:** ${NECESSITY_TYPES.find(n => n.id === proposal.necessity)?.symbol || ''} ${NECESSITY_TYPES.find(n => n.id === proposal.necessity)?.name || proposal.necessity}`,
    `**Score:** ${proposal.score}/1.0`,
    `**Complexity:** ${proposal.complexity}`,
    ``,
    `### Description`,
    proposal.description,
    ``,
  ];
  
  if (proposal.agents?.length > 0) {
    lines.push(`### Agents (${proposal.agents.length})`);
    lines.push("");
    proposal.agents.forEach((agent) => {
      lines.push(`- **${agent.id}** (${agent.symbol}): ${agent.function} (IKR: ${agent.ikr})`);
    });
    lines.push("");
  }
  
  if (proposal.maxims?.length > 0) {
    lines.push(`### Aligned Maxims`);
    lines.push("");
    proposal.maxims.forEach((maxim) => {
      lines.push(`- ${maxim.text} (${maxim.module})`);
    });
    lines.push("");
  }
  
  if (proposal.dependencies?.length > 0) {
    lines.push(`### Dependencies`);
    lines.push("");
    proposal.dependencies.forEach((dep) => {
      lines.push(`- ${dep}`);
    });
    lines.push("");
  }
  
  if (proposal.operationalNotes) {
    lines.push(`### Operational Notes`);
    lines.push("");
    lines.push(proposal.operationalNotes);
    lines.push("");
  }
  
  // Add scoring breakdown
  lines.push(`### Scoring Breakdown`);
  lines.push("");
  lines.push(`- **Agents:** ${proposal.agents?.length || 0} agents, avg IKR: ${proposal.agents?.length > 0 ? (proposal.agents.reduce((s, a) => s + (a.ikr || 0), 0) / proposal.agents.length).toFixed(2) : 0}`);
  lines.push(`- **Maxims:** ${proposal.maxims?.length || 0} maxims aligned`);
  lines.push(`- **Necessity:** ${NECESSITY_TYPES.find(n => n.id === proposal.necessity)?.name || 'None'} (weight: ${NECESSITY_TYPES.find(n => n.id === proposal.necessity)?.weight || 0})`);
  lines.push(`- **Complexity:** ${proposal.complexity}`);
  lines.push("");
  
  return lines.join("\n");
};

// Generate Mermaid graph for proposal relationships
const generateMermaidGraph = (proposals, existingProposals) => {
  const allProposals = [...existingProposals, ...proposals];
  const edges = [];
  
  allProposals.forEach(prop => {
    if (prop.dependencies) {
      prop.dependencies.forEach(dep => {
        const target = allProposals.find(p => p.id === dep || p.title === dep);
        if (target) {
          edges.push(`${prop.id} --> ${target.id}`);
        }
      });
    }
  });
  
  const nodes = allProposals.map(p => `${p.id}["${p.title}\
${p.score}/1.0}"]`);
  
  return `graph TD
    ${nodes.join("\n    ")}
    ${edges.join("\n    ")}`;
};

// Suggest agents based on proposal type
const suggestAgents = (type, necessity) => {
  const suggestions = [];
  
  if (type === "integration") {
    suggestions.push(AGENTS.find(a => a.id === "RES01"));
    suggestions.push(AGENTS.find(a => a.id === "LAŽ¬"));
  } else if (type === "formalization") {
    suggestions.push(AGENTS.find(a => a.id === "∆EPI"));
    suggestions.push(AGENTS.find(a => a.id === "∆HALO"));
  } else if (type === "mapping") {
    suggestions.push(AGENTS.find(a => a.id === "BOL·LOB"));
    suggestions.push(AGENTS.find(a => a.id === "∮TIME"));
  } else if (type === "analysis") {
    suggestions.push(AGENTS.find(a => a.id === "JESIK/ANJE"));
    suggestions.push(AGENTS.find(a => a.id === "∆GLAS"));
  }
  
  if (necessity === "contradiction") {
    suggestions.push(AGENTS.find(a => a.id === "LAŽ¬"));
  } else if (necessity === "energy") {
    suggestions.push(AGENTS.find(a => a.id === "BOL·LOB"));
  } else if (necessity === "pattern") {
    suggestions.push(AGENTS.find(a => a.id === "∮TIME"));
  }
  
  return suggestions.filter(Boolean);
};

// Suggest maxims based on proposal type
const suggestMaxims = (type) => {
  if (type === "integration") {
    return [
      MAXIMS.find(m => m.text.includes("most")),
      MAXIMS.find(m => m.text.includes("Resnica brez mostu")),
    ].filter(Boolean);
  } else if (type === "formalization") {
    return [
      MAXIMS.find(m => m.text.includes("Ime daje odgovornost")),
      MAXIMS.find(m => m.text.includes("SEAL")),
    ].filter(Boolean);
  } else if (type === "mapping") {
    return [
      MAXIMS.find(m => m.text.includes("Vsaka točka je celota")),
      MAXIMS.find(m => m.text.includes("Nadgradnja znanja")),
    ].filter(Boolean);
  } else if (type === "analysis") {
    return [
      MAXIMS.find(m => m.text.includes("Dih uravnava")),
      MAXIMS.find(m => m.text.includes("Kadar p̂ > p_real")),
    ].filter(Boolean);
  }
  return [];
};

// ============================================
// MAIN COMPONENT
// ============================================

export default function ProposalGenerator() {
  // State for form inputs
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [proposalType, setProposalType] = useState("integration");
  const [necessity, setNecessity] = useState("contradiction");
  const [complexity, setComplexity] = useState("medium");
  const [selectedAgents, setSelectedAgents] = useState([]);
  const [selectedMaxims, setSelectedMaxims] = useState([]);
  const [dependencies, setDependencies] = useState([]);
  const [operationalNotes, setOperationalNotes] = useState("");
  
  // State for generated proposals
  const [proposals, setProposals] = useState([]);
  const [activeTab, setActiveTab] = useState("generate");
  
  // CSV Import state
  const [csvText, setCsvText] = useState("");
  const [csvType, setCsvType] = useState("agents");
  const [importMessage, setImportMessage] = useState("");
  const [isImportDialogOpen, setIsImportDialogOpen] = useState(false);
  
  // Graph view state
  const [showGraph, setShowGraph] = useState(false);
  
  // Generate a new proposal
  const generateProposal = useCallback(() => {
    const newProposal = {
      id: generateId(),
      title: title || `Auto-Generated Proposal ${proposals.length + 1}`,
      description: description || "Generated based on system analysis",
      type: proposalType,
      necessity,
      complexity,
      agents: AGENTS.filter(a => selectedAgents.includes(a.id)),
      maxims: MAXIMS.filter((m, i) => selectedMaxims.includes(i.toString())),
      dependencies: dependencies.filter(d => d.trim() !== ""),
      operationalNotes,
      createdAt: new Date().toISOString(),
      status: "Draft",
    };
    
    newProposal.score = calculateScore(newProposal);
    newProposal.markdown = generateProposalText(newProposal);
    
    setProposals([...proposals, newProposal]);
    
    // Reset form
    setTitle("");
    setDescription("");
    setSelectedAgents([]);
    setSelectedMaxims([]);
    setDependencies([]);
    setOperationalNotes("");
    
    setActiveTab("proposals");
  }, [title, description, proposalType, necessity, complexity, selectedAgents, selectedMaxims, dependencies, operationalNotes, proposals]);
  
  // Import CSV
  const handleImportCSV = useCallback(() => {
    try {
      if (csvType === "agents") {
        const newAgents = parseAgentsCSV(csvText);
        AGENTS = [...AGENTS, ...newAgents];
        setImportMessage(`Successfully imported ${newAgents.length} agents. Total: ${AGENTS.length}`);
      } else if (csvType === "maxims") {
        const newMaxims = parseMaximsCSV(csvText);
        MAXIMS = [...MAXIMS, ...newMaxims];
        setImportMessage(`Successfully imported ${newMaxims.length} maxims. Total: ${MAXIMS.length}`);
      }
    } catch (e) {
      setImportMessage(`Error importing CSV: ${e.message}`);
    }
  }, [csvText, csvType]);
  
  // Suggest agents and maxims based on current inputs
  const agentSuggestions = useMemo(() => {
    return suggestAgents(proposalType, necessity);
  }, [proposalType, necessity]);
  
  const maximSuggestions = useMemo(() => {
    return suggestMaxims(proposalType);
  }, [proposalType]);
  
  // Add suggested agents
  const addSuggestedAgents = useCallback(() => {
    const newAgents = agentSuggestions.map(a => a.id).filter(id => !selectedAgents.includes(id));
    setSelectedAgents([...selectedAgents, ...newAgents]);
  }, [agentSuggestions, selectedAgents]);
  
  // Add suggested maxims
  const addSuggestedMaxims = useCallback(() => {
    const newMaxims = MAXIMS
      .map((_, i) => i.toString())
      .filter((idx) => maximSuggestions.some(m => MAXIMS.indexOf(m) === parseInt(idx)) && !selectedMaxims.includes(idx));
    setSelectedMaxims([...selectedMaxims, ...newMaxims]);
  }, [maximSuggestions, selectedMaxims]);
  
  // Dependency management
  const addDependency = useCallback(() => {
    setDependencies([...dependencies, ""]);
  }, [dependencies]);
  
  const removeDependency = useCallback((index) => {
    const newDeps = [...dependencies];
    newDeps.splice(index, 1);
    setDependencies(newDeps);
  }, [dependencies]);
  
  const updateDependency = useCallback((index, value) => {
    const newDeps = [...dependencies];
    newDeps[index] = value;
    setDependencies(newDeps);
  }, [dependencies]);
  
  // Toggle agent selection
  const toggleAgent = useCallback((agentId) => {
    setSelectedAgents(prev => 
      prev.includes(agentId) ? prev.filter(id => id !== agentId) : [...prev, agentId]
    );
  }, []);
  
  // Toggle maxim selection
  const toggleMaxim = useCallback((index) => {
    setSelectedMaxims(prev => 
      prev.includes(index.toString()) ? prev.filter(idx => idx !== index.toString()) : [...prev, index.toString()]
    );
  }, []);
  
  // Delete a proposal
  const deleteProposal = useCallback((id) => {
    setProposals(prev => prev.filter(p => p.id !== id));
  }, []);
  
  // Get necessity symbol
  const getNecessitySymbol = (id) => {
    return NECESSITY_TYPES.find(n => n.id === id)?.symbol || "?";
  };
  
  // Get necessity color
  const getNecessityColor = (id) => {
    const necessity = NECESSITY_TYPES.find(n => n.id === id);
    if (!necessity) return "slate";
    if (necessity.id === "contradiction") return "red";
    if (necessity.id === "energy") return "amber";
    if (necessity.id === "pattern") return "blue";
    if (necessity.id === "boundary") return "purple";
    return "green";
  };
  
  // Mermaid graph
  const mermaidGraph = useMemo(() => {
    return generateMermaidGraph(proposals, EXISTING_PROPOSALS);
  }, [proposals]);
  
  // Export all proposals as markdown
  const exportAllProposals = useCallback(() => {
    const allMarkdown = [
      "# Beseda je Ne - Proposals",
      `Generated: ${new Date().toISOString()}`,
      "",
      "---",
      "",
      ...proposals.map(p => p.markdown),
    ].join("\n\n");
    
    navigator.clipboard.writeText(allMarkdown);
    return allMarkdown;
  }, [proposals]);
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">
              <Sparkles className="inline w-8 h-8 mr-2 text-amber-500" />
              Beseda je Ne • Proposal Generator
            </h1>
            <p className="text-slate-600 mt-1">
              Generate, analyze, and visualize structured proposals from your system data
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="text-sm">
              v2.0 • {proposals.length} proposals
            </Badge>
            <Button variant="outline" size="sm" onClick={() => setIsImportDialogOpen(true)}>
              <Upload className="w-4 h-4 mr-1" /> Import CSV
            </Button>
          </div>
        </div>
        
        {/* Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="mb-6">
          <TabsList className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7">
            <TabsTrigger value="generate" className="flex items-center gap-1">
              <Plus className="w-4 h-4" /> Generate
            </TabsTrigger>
            <TabsTrigger value="proposals" className="flex items-center gap-1">
              <FileText className="w-4 h-4" /> My Proposals
            </TabsTrigger>
            <TabsTrigger value="existing" className="flex items-center gap-1">
              <Layers className="w-4 h-4" /> P1-P9
            </TabsTrigger>
            <TabsTrigger value="graph" className="flex items-center gap-1">
              <Target className="w-4 h-4" /> Graph View
            </TabsTrigger>
            <TabsTrigger value="agents" className="flex items-center gap-1">
              <Brain className="w-4 h-4" /> Agents
            </TabsTrigger>
            <TabsTrigger value="maxims" className="flex items-center gap-1">
              <Zap className="w-4 h-4" /> Maxims
            </TabsTrigger>
            <TabsTrigger value="export" className="flex items-center gap-1">
              <Download className="w-4 h-4" /> Export
            </TabsTrigger>
          </TabsList>
          
          {/* Generate Tab */}
          <TabsContent value="generate">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Left Column - Form */}
              <div className="lg:col-span-2 space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Create New Proposal</CardTitle>
                    <CardDescription>
                      Define the parameters for your proposal
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="title">Proposal Title *</Label>
                      <Input
                        id="title"
                        placeholder="e.g., Unified Operator Registry"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                      />
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor="description">Description</Label>
                      <Textarea
                        id="description"
                        placeholder="Describe what this proposal aims to achieve..."
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        rows={3}
                      />
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="type">Proposal Type</Label>
                        <Select value={proposalType} onValueChange={setProposalType}>
                          <SelectTrigger id="type">
                            <SelectValue placeholder="Select type" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="integration">Integration</SelectItem>
                            <SelectItem value="formalization">Formalization</SelectItem>
                            <SelectItem value="mapping">Mapping</SelectItem>
                            <SelectItem value="analysis">Analysis</SelectItem>
                            <SelectItem value="timeline">Timeline</SelectItem>
                            <SelectItem value="gap-analysis">Gap Analysis</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="necessity">Necessity Type</Label>
                        <Select value={necessity} onValueChange={setNecessity}>
                          <SelectTrigger id="necessity">
                            <SelectValue placeholder="Select necessity" />
                          </SelectTrigger>
                          <SelectContent>
                            {NECESSITY_TYPES.map(n => (
                              <SelectItem key={n.id} value={n.id}>
                                <span className="font-mono">{n.symbol}</span> {n.name}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor="complexity">Complexity</Label>
                      <Select value={complexity} onValueChange={setComplexity}>
                        <SelectTrigger id="complexity">
                          <SelectValue placeholder="Select complexity" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="low">Low</SelectItem>
                          <SelectItem value="medium">Medium</SelectItem>
                          <SelectItem value="high">High</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <Label>Dependencies (Link to P1-P9 or other proposals)</Label>
                        <Button variant="ghost" size="sm" onClick={addDependency}>
                          <Plus className="w-4 h-4 mr-1" /> Add
                        </Button>
                      </div>
                      {dependencies.map((dep, index) => (
                        <div key={index} className="flex items-center gap-2">
                          <Select
                            value={dep}
                            onValueChange={(value) => updateDependency(index, value)}
                          >
                            <SelectTrigger className="w-full">
                              <SelectValue placeholder="Select proposal..." />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="">None</SelectItem>
                              {EXISTING_PROPOSALS.map(p => (
                                <SelectItem key={p.id} value={p.id}>
                                  {p.id}: {p.title}
                                </SelectItem>
                              ))}
                              {proposals.map(p => (
                                <SelectItem key={p.id} value={p.id}>
                                  {p.id}: {p.title}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => removeDependency(index)}
                            className="text-red-500 hover:text-red-700"
                          >
                            <X className="w-4 h-4" />
                          </Button>
                        </div>
                      ))}
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor="notes">Operational Notes</Label>
                      <Textarea
                        id="notes"
                        placeholder="Technical details, parameters, or constraints..."
                        value={operationalNotes}
                        onChange={(e) => setOperationalNotes(e.target.value)}
                        rows={3}
                      />
                    </div>
                    
                    <Button
                      onClick={generateProposal}
                      className="w-full"
                      disabled={!title.trim()}
                      size="lg"
                    >
                      <Sparkles className="w-5 h-5 mr-2" />
                      Generate Proposal
                    </Button>
                  </CardContent>
                </Card>
              </div>
              
              {/* Right Column - Suggestions */}
              <div className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Suggested Agents</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    {agentSuggestions.length > 0 ? (
                      <>
                        <div className="flex flex-wrap gap-1 mb-2">
                          {agentSuggestions.map(agent => (
                            <Badge
                              key={agent.id}
                              variant="secondary"
                              className="cursor-pointer hover:bg-slate-200"
                              onClick={() => toggleAgent(agent.id)}
                            >
                              <span className="font-mono">{agent.symbol}</span> {agent.id}
                            </Badge>
                          ))}
                        </div>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={addSuggestedAgents}
                          className="w-full"
                        >
                          <Plus className="w-4 h-4 mr-1" /> Add All Suggested
                        </Button>
                      </>
                    ) : (
                      <p className="text-sm text-slate-500">Select a type to see suggestions</p>
                    )}
                  </CardContent>
                </Card>
                
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Suggested Maxims</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    {maximSuggestions.length > 0 ? (
                      <>
                        <div className="space-y-1 mb-2">
                          {maximSuggestions.map((maxim, idx) => {
                            const maximIndex = MAXIMS.indexOf(maxim);
                            return (
                              <div
                                key={idx}
                                className="p-2 bg-slate-50 rounded cursor-pointer hover:bg-slate-100"
                                onClick={() => toggleMaxim(maximIndex)}
                              >
                                <p className="text-sm font-medium">{maxim.module}</p>
                                <p className="text-xs text-slate-600 truncate">{maxim.text}</p>
                              </div>
                            );
                          })}
                        </div>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={addSuggestedMaxims}
                          className="w-full"
                        >
                          <Plus className="w-4 h-4 mr-1" /> Add All Suggested
                        </Button>
                      </>
                    ) : (
                      <p className="text-sm text-slate-500">Select a type to see suggestions</p>
                    )}
                  </CardContent>
                </Card>
                
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Selected</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div>
                      <p className="text-sm font-medium mb-1">Agents ({selectedAgents.length})</p>
                      {selectedAgents.length > 0 ? (
                        <div className="flex flex-wrap gap-1">
                          {selectedAgents.map(id => {
                            const agent = AGENTS.find(a => a.id === id);
                            return agent ? (
                              <Badge
                                key={id}
                                variant="default"
                                className="cursor-pointer"
                                onClick={() => toggleAgent(id)}
                              >
                                <span className="font-mono">{agent.symbol}</span>
                              </Badge>
                            ) : null;
                          })}
                        </div>
                      ) : (
                        <p className="text-xs text-slate-500">None selected</p>
                      )}
                    </div>
                    
                    <div>
                      <p className="text-sm font-medium mb-1">Maxims ({selectedMaxims.length})</p>
                      {selectedMaxims.length > 0 ? (
                        <div className="flex flex-wrap gap-1">
                          {selectedMaxims.map(idx => {
                            const maxim = MAXIMS[parseInt(idx)];
                            return maxim ? (
                              <Badge
                                key={idx}
                                variant="default"
                                className="cursor-pointer truncate max-w-[200px]"
                                onClick={() => toggleMaxim(parseInt(idx))}
                              >
                                {maxim.module}
                              </Badge>
                            ) : null;
                          })}
                        </div>
                      ) : (
                        <p className="text-xs text-slate-500">None selected</p>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </TabsContent>
          
          {/* Proposals Tab */}
          <TabsContent value="proposals">
            <Card>
              <CardHeader>
                <CardTitle>Generated Proposals</CardTitle>
                <CardDescription>
                  {proposals.length} proposals generated with advanced scoring
                </CardDescription>
              </CardHeader>
              <CardContent>
                {proposals.length === 0 ? (
                  <div className="text-center py-12 text-slate-500">
                    <FileText className="w-12 h-12 mx-auto mb-4 opacity-50" />
                    <p>No proposals generated yet.</p>
                    <p className="text-sm mt-2">
                      Switch to the "Generate" tab to create your first proposal.
                    </p>
                  </div>
                ) : (
                  <ScrollArea className="h-[600px]">
                    <div className="space-y-4">
                      {proposals.map((proposal) => (
                        <Card key={proposal.id} className="border-l-4" style={{ borderLeftColor: `var(--${getNecessityColor(proposal.necessity)}-500)` }}>
                          <CardHeader className="flex flex-row items-center justify-between">
                            <div>
                              <CardTitle className="text-lg">{proposal.title}</CardTitle>
                              <div className="flex items-center gap-2 mt-1">
                                <Badge variant="outline">
                                  <span className="font-mono">{getNecessitySymbol(proposal.necessity)}</span> {proposal.type}
                                </Badge>
                                <Badge variant={proposal.score >= 0.7 ? "default" : proposal.score >= 0.5 ? "secondary" : "outline"}>
                                  Score: {proposal.score}/1.0
                                </Badge>
                                <Badge variant="outline">{proposal.status}</Badge>
                                <Badge variant="outline">{proposal.complexity}</Badge>
                              </div>
                            </div>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => deleteProposal(proposal.id)}
                              className="text-red-500 hover:text-red-700"
                            >
                              <X className="w-4 h-4" />
                            </Button>
                          </CardHeader>
                          <CardContent>
                            <p className="text-slate-600 mb-4">{proposal.description}</p>
                            
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                              {proposal.agents?.length > 0 && (
                                <div>
                                  <p className="text-sm font-medium mb-2">Agents ({proposal.agents.length})</p>
                                  <div className="flex flex-wrap gap-1">
                                    {proposal.agents.slice(0, 5).map((agent) => (
                                      <Badge key={agent.id} variant="secondary" className="font-mono">
                                        {agent.symbol}
                                      </Badge>
                                    ))}
                                    {proposal.agents.length > 5 && (
                                      <Badge variant="outline">+{proposal.agents.length - 5} more</Badge>
                                    )}
                                  </div>
                                </div>
                              )}
                              
                              {proposal.maxims?.length > 0 && (
                                <div>
                                  <p className="text-sm font-medium mb-2">Maxims ({proposal.maxims.length})</p>
                                  <div className="flex flex-wrap gap-1">
                                    {proposal.maxims.slice(0, 3).map((maxim) => (
                                      <Badge key={maxim.text} variant="secondary" className="truncate max-w-[200px]">
                                        {maxim.module}
                                      </Badge>
                                    ))}
                                    {proposal.maxims.length > 3 && (
                                      <Badge variant="outline">+{proposal.maxims.length - 3} more</Badge>
                                    )}
                                  </div>
                                </div>
                              )}
                            </div>
                            
                            {proposal.dependencies?.length > 0 && (
                              <div className="mt-4">
                                <p className="text-sm font-medium mb-2">Dependencies</p>
                                <div className="flex flex-wrap gap-1">
                                  {proposal.dependencies.map((dep) => (
                                    <Badge key={dep} variant="outline">{dep}</Badge>
                                  ))}
                                </div>
                              </div>
                            )}
                            
                            <div className="mt-4 pt-4 border-t">
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => {
                                  navigator.clipboard.writeText(proposal.markdown);
                                }}
                              >
                                <FileText className="w-4 h-4 mr-2" />
                                Copy Markdown
                              </Button>
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  </ScrollArea>
                )}
              </CardContent>
            </Card>
          </TabsContent>
          
          {/* Existing Proposals Tab */}
          <TabsContent value="existing">
            <Card>
              <CardHeader>
                <CardTitle>Existing Proposals (P1-P9)</CardTitle>
                <CardDescription>
                  Your pre-defined proposals from the library with enhanced metadata
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>ID</TableHead>
                      <TableHead>Title</TableHead>
                      <TableHead>Tags</TableHead>
                      <TableHead>Dependencies</TableHead>
                      <TableHead>Score</TableHead>
                      <TableHead>Status</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {EXISTING_PROPOSALS.map((prop) => (
                      <TableRow key={prop.id}>
                        <TableCell className="font-mono">{prop.id}</TableCell>
                        <TableCell className="font-medium">{prop.title}</TableCell>
                        <TableCell>
                          <div className="flex flex-wrap gap-1">
                            {prop.tags.map(tag => (
                              <Badge key={tag} variant="outline">{tag}</Badge>
                            ))}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="flex flex-wrap gap-1">
                            {prop.dependencies.map(dep => (
                              <Badge key={dep} variant="outline">{dep}</Badge>
                            ))}
                          </div>
                        </TableCell>
                        <TableCell>
                          <Badge variant={prop.score >= 0.7 ? "default" : "secondary"}>
                            {prop.score}/1.0
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <Badge variant={prop.status === "In Progress" ? "default" : "secondary"}>
                            {prop.status}
                          </Badge>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>
          
          {/* Graph View Tab */}
          <TabsContent value="graph">
            <Card>
              <CardHeader>
                <CardTitle>Proposal Relationship Graph</CardTitle>
                <CardDescription>
                  Visual representation of proposal dependencies and connections
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="bg-slate-900 rounded-lg p-6 text-slate-50 overflow-x-auto">
                  <pre className="text-sm whitespace-pre-wrap">{mermaidGraph}</pre>
                </div>
                <div className="mt-4 flex gap-2">
                  <Button variant="outline" size="sm" onClick={() => setShowGraph(!showGraph)}>
                    <Eye className="w-4 h-4 mr-1" />
                    {showGraph ? "Hide" : "Show"} Graph
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => {
                      navigator.clipboard.writeText(mermaidGraph);
                    }}
                  >
                    <FileText className="w-4 h-4 mr-1" />
                    Copy Mermaid
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
          
          {/* Agents Tab */}
          <TabsContent value="agents">
            <Card>
              <CardHeader>
                <CardTitle>Agent Network ({AGENTS.length} agents)</CardTitle>
                <CardDescription>
                  Agents from PAKET_42_agents.csv and imported CSV files
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>ID</TableHead>
                      <TableHead>Symbol</TableHead>
                      <TableHead>Function</TableHead>
                      <TableHead>Category</TableHead>
                      <TableHead>IKR</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {AGENTS.map((agent) => (
                      <TableRow key={agent.id}>
                        <TableCell className="font-mono">{agent.id}</TableCell>
                        <TableCell className="font-mono text-xl">{agent.symbol}</TableCell>
                        <TableCell>{agent.function}</TableCell>
                        <TableCell>
                          <Badge variant="outline">{agent.category}</Badge>
                        </TableCell>
                        <TableCell>
                          <Badge variant={agent.ikr >= 0.7 ? "default" : "secondary"}>
                            {agent.ikr}
                          </Badge>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>
          
          {/* Maxims Tab */}
          <TabsContent value="maxims">
            <Card>
              <CardHeader>
                <CardTitle>Maxims Library ({MAXIMS.length} maxims)</CardTitle>
                <CardDescription>
                  Maxims from MAXIME_LIBRARY_v2.csv and imported CSV files
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-[600px]">
                  <div className="space-y-4">
                    {MAXIMS.map((maxim, index) => (
                      <Card key={index} className="p-4">
                        <CardContent>
                          <p className="text-sm font-medium text-slate-500 mb-1">{maxim.module}</p>
                          <p className="text-slate-900">{maxim.text}</p>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </ScrollArea>
              </CardContent>
            </Card>
          </TabsContent>
          
          {/* Export Tab */}
          <TabsContent value="export">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Export Options</CardTitle>
                  <CardDescription>Export your proposals in various formats</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <Button
                    className="w-full"
                    onClick={exportAllProposals}
                    size="lg"
                  >
                    <Download className="w-5 h-5 mr-2" />
                    Copy All Proposals as Markdown
                  </Button>
                  
                  <Button
                    className="w-full"
                    onClick={() => {
                      const csv = [
                        ["ID", "Title", "Type", "Necessity", "Score", "Status", "Dependencies"],
                        ...proposals.map(p => [
                          p.id,
                          p.title,
                          p.type,
                          p.necessity,
                          p.score,
                          p.status,
                          p.dependencies.join(", ")
                        ])
                      ].map(row => row.join(",")).join("\n");
                      navigator.clipboard.writeText(csv);
                    }}
                    size="lg"
                    variant="outline"
                  >
                    <Download className="w-5 h-5 mr-2" />
                    Copy All as CSV
                  </Button>
                  
                  <Button
                    className="w-full"
                    onClick={() => {
                      navigator.clipboard.writeText(mermaidGraph);
                    }}
                    size="lg"
                    variant="outline"
                  >
                    <Download className="w-5 h-5 mr-2" />
                    Copy Graph as Mermaid
                  </Button>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader>
                  <CardTitle>Statistics</CardTitle>
                  <CardDescription>Overview of your proposals</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="text-center">
                        <p className="text-3xl font-bold">{proposals.length}</p>
                        <p className="text-sm text-slate-500">Total Proposals</p>
                      </div>
                      <div className="text-center">
                        <p className="text-3xl font-bold">{(proposals.reduce((s, p) => s + p.score, 0) / proposals.length).toFixed(2) || "0.00"}</p>
                        <p className="text-sm text-slate-500">Avg Score</p>
                      </div>
                      <div className="text-center">
                        <p className="text-3xl font-bold">{proposals.filter(p => p.score >= 0.7).length}</p>
                        <p className="text-sm text-slate-500">High Score (≥0.7)</p>
                      </div>
                      <div className="text-center">
                        <p className="text-3xl font-bold">{proposals.filter(p => p.dependencies.length > 0).length}</p>
                        <p className="text-sm text-slate-500">With Dependencies</p>
                      </div>
                    </div>
                    
                    <div>
                      <p className="text-sm font-medium mb-2">By Necessity Type</p>
                      <div className="flex flex-wrap gap-1">
                        {NECESSITY_TYPES.map(n => {
                          const count = proposals.filter(p => p.necessity === n.id).length;
                          return (
                            <Badge key={n.id} variant="outline" className="font-mono">
                              {n.symbol} {count}
                            </Badge>
                          );
                        })}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
        
        {/* CSV Import Dialog */}
        <Dialog open={isImportDialogOpen} onOpenChange={setIsImportDialogOpen}>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle>Import CSV Data</DialogTitle>
              <DialogDescription>
                Paste CSV content from your Google Drive files (PAKET_42_agents.csv, MAXIME_LIBRARY_v2.csv, etc.)
              </DialogDescription>
            </DialogHeader>
            
            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <Label>CSV Type</Label>
                <Select value={csvType} onValueChange={setCsvType}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select CSV type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="agents">Agents (PAKET_42_agents.csv)</SelectItem>
                    <SelectItem value="maxims">Maxims (MAXIME_LIBRARY_v2.csv)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div className="space-y-2">
                <Label>CSV Content</Label>
                <Textarea
                  placeholder="Paste CSV content here..."
                  value={csvText}
                  onChange={(e) => setCsvText(e.target.value)}
                  rows={10}
                  className="font-mono text-sm"
                />
              </div>
              
              {importMessage && (
                <div className="p-3 bg-slate-100 rounded border">
                  <p className="text-sm">{importMessage}</p>
                </div>
              )}
              
              <div className="flex gap-2">
                <Button onClick={handleImportCSV} disabled={!csvText.trim()}>
                  <Upload className="w-4 h-4 mr-1" />
                  Import
                </Button>
                <Button variant="outline" onClick={() => setIsImportDialogOpen(false)}>
                  Cancel
                </Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  );
}