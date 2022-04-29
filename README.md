# Auto-transformer

## Input

### User Input

- Input Voltage $V_{in}$
- Output Power $P_o=250$
- Frequency $f=47$
- Efficiency $\eta=95\%$
- Operating flux density $B_{ac}$
- Temperature rise goal, $T_r=30^oC$
- Window utilization, $K_u=0.4$
- Core Material = $Silicon M6X$
- Lamination Number = $EI-150$
- Current Density $J$

### Constants 

- Window utilization $K_u$

## Apparent Power $P_t$

Calculating the transformer apparent power, $P_t$

$$ P_t=P_o(\dfrac{1}{\eta} + 1), [watts]$$

$$P_t=250[(1/0.95)+1]$$

$$P_t=513, [watts]$$

## Calculation of Area Product

$$J=\dfrac{P_t (10^4)}{K_f K_u B_ac f A_p} $$

$$A_p=\dfrac{P_t (10^4)}{K_f K_u B_ac f J} $$

---
## Project files


<pre>
.
&#8866; README.md
&#8866; DATA
    &#8866; EI-Laminations.csv
    &#8985; EMD - Sheet1.csv
&#8866; FINAL
    &#8866; DATA
       &#8866; EI-Laminations.csv
        &#8985; EMD - Sheet1.csv    
    &#8866; data.py
    &#8985; main.py
&#8866; TEST
&#8866; .gitignore
&#8866; main.ipynb
&#8866; main.py
&#8866; requirements.txt
&#8985; sop.txt
</pre>