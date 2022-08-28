
class FSMn:
    def __init__(
        self,
        Q : set,   # Conjunto de estados
        Σ : set,   # Alfabetos
        δ : dict,  # Tabela de transições
        q0 : str,  # Estado inicial
        F : set    # Estados finais
    ) -> None:
        self.Q = Q
        self.Σ = Σ
        self.δ = δ
        self.q0 = q0
        self.F = F
    
    
    def evaluate(self, word : str) -> bool:
        Q = { self.q0 }
        
        for sym in word:
            new = set()
            for q in Q:
                if sym in self.δ[q]:
                    for q1 in self.δ[q][sym]:
                        new.add(q1)
            Q = new
        
        return len(Q & self.F) > 0


class FSMε:
    def __init__(
        self,
        Q : set,   # Conjunto de estados
        Σ : set,   # Alfabetos
        δ : dict,  # Tabela de transições
        q0 : str,  # Estado inicial
        F : set    # Estados finais
    ) -> None:
        self.Q = Q
        self.Σ = Σ
        self.δ = δ
        self.q0 = q0
        self.F = F
    
    
    def _εReachable(self, state : set) -> set:
        S = set(state)
        queue = list(state)
        
        while len(queue) > 0:
            q = queue.pop()
            if ('ε' in self.δ[q]):
                new = self.δ[q]['ε'] - S
                S.update(new)
                queue.extend(new)
        
        return S
    
    
    def evaluate(self, word : str) -> bool:
        Q = self._εReachable({ self.q0 })
        for c in word:
            new = set()
            for q in Q:
                if c in self.δ[q]:
                    new.update(self._εReachable(self.δ[q][c]))
            
            Q = new
        return len(Q & self.F) > 0
    
    
    def convertToFSMn(self):
        newF = set(self.F)
        newδ = dict()
        
        for q, t in self.δ.items():
            newδ[q] = dict()
            for symbol, transitions in t.items():
                if symbol != 'ε':
                    newδ[symbol] = transitions
        
        for q in self.Q:
            reachable = self._εReachable({ q })
            reachable.remove(q)
            if reachable & self.F:
                newF.add(q)
            
            for q1 in reachable:
                for sym in self.Σ:
                    if sym not in newδ[q]: newδ[q][sym] = set()
                    newδ[q][sym].add(q1)
        
        return FSMn(self.Q, self.Σ, newδ, self.q0, newF)


def main():
    word = "abbab"
    
    Q = { 0, 1, 2 }
    Σ = { 'a', 'b' }
    δ = { 
        0:{ 'ε':{1},
            'a':{0}},

        1:{ 'b':{1},
            'ε':{2}},

        2:{ 'a':{2}}
    }
    q0 = 0
    F = { 2 }
    
    fsme = FSMε(Q, Σ, δ, q0, F)
    print(fsme.evaluate(word))
    
    fsmn = fsme.convertToFSMn()
    print(fsmn.evaluate(word))


if __name__ == "__main__":
    main()