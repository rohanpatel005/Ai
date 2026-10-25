# Medical AI Ethics, Safety & Governance Documentation

**Course:** ECSCT24301 – Foundation of AI  
**Track:** Applied AI Project Track  
**Institution:** Adani University  

---

## 1. Educational AI Prototype Boundary
This software is strictly an academic research prototype developed for educational demonstration in course ECSCT24301 (Foundation of AI). It is **explicitly NOT a certified medical diagnostic device, clinical decision-support software, or triage system**.

### Prohibited Usages:
- The system must NEVER be used to make clinical treatment decisions.
- The system must NEVER prescribe or recommend medications or drug dosages.
- The system must NEVER provide definitive assertions of clinical certainty (e.g., "You have disease X").
- The system must NEVER replace consultations with qualified, licensed medical professionals.

---

## 2. Safety Language Protocol
The system enforces standardized ethical phrasing across all interfaces and outputs:
- **Positive Inference:** *"Based on the selected symptoms and the implemented knowledge rules, the system inferred..."* or *"The current knowledge base contains supporting rules for..."*
- **Insufficient Evidence:** *"Insufficient information for a rule-based inference."*
- **Competing Evidence:** *"Multiple hypotheses are supported by the current knowledge base."*

---

## 3. Data Privacy & Patient Confidentiality
- **Zero Protected Health Information (PHI):** The system strictly does not store, process, or transmit personal health data, patient identifiers, names, medical record numbers, or biometric information.
- **Open-Access Benchmark Data Only:** Evaluation is conducted solely on de-identified, publicly licensed academic datasets (Kaggle / Mendeley Data).

---

## 4. Conflict Resolution & Differential Safety
When patient symptoms match rules for multiple distinct medical conditions, automated diagnostic systems risk premature closure or erroneous confirmation bias if a single disease is silently selected.
To mitigate this risk, our **Conflict Resolution Subsystem** guarantees that whenever multiple hypotheses are supported, **all** supported hypotheses are transparently displayed alongside their individual premise matches, evidence weights, and medical citations.

---

## 5. Algorithmic Bias & Sourcing Transparency
- All medical IF-THEN rules are mapped to publicly accessible, verified clinical guidelines from the World Health Organization (WHO), Centers for Disease Control and Prevention (CDC), and National Health Service (NHS).
- Rule sources and URLs are displayed directly in the user interface to ensure full provenance traceability.
