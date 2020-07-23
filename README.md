# Population coverage of a vaccine targeting HIV-1 PCS [Analysis]

This project involved using validated epitope data to assess the population coverage of a
potential HIV-1 vaccine targeting the protease cleavage sites (PCS) (all PCS, Gag PCS, or Pol PCS).

The data on population coverage, average epitope hit per individual, and minimum number of epitopes recognized by 90% of the population (PC90) was obtained from IEDB[http://tools.iedb.org/population/] and can be found in the <code>Country</code> and <code>Regions</code> directories; the raw data is not labelled, however, the output is.

This script conducts ANOVA and Fisher's exact testing to examine for significance between the three epitope sets (all PCS, Gag PCS, and Pol PCS) in regards to coverage (Fisher's), average hit (anova), and PC90 (anova).

# Dependencies

<ul>
  <li>Python 3+</li>
  <li>Pandas</li>
  <li>Numpy</li>
  <li>Scipy</li>
</ul>

# Use

After cloning the repository, navigate to the directory via your terminal and execute <code>analysis.py</code>

# Output

Pandas DataFrame with population coverage, average hit, and PC90 raw data displayed with P values.
