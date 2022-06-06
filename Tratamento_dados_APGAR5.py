#!/usr/bin/env python
# coding: utf-8

# # Módulo 5 Tarefa 1
# ## Base de nascidos vivos do DataSUS
# O DataSUS disponibiliza diversos arquivos de dados com relação a seus segurados, conforme a [lei da transparência de informações públicas](https://www.sisgov.com/transparencia-acesso-informacao/#:~:text=A%20Lei%20da%20Transpar%C3%AAncia%20(LC,em%20um%20site%20na%20internet.). 
# 
# Essas informações podem ser obtidas pela internet [aqui](http://www2.datasus.gov.br/DATASUS/index.php?area=0901&item=1). Como o processo de obtenção desses arquivos foge um pouco do nosso escopo, deixamos o arquivo ```SINASC_RO_2019.csv``` já como vai ser encontrado no DataSUS. O dicionário de dados está no arquivo ```estrutura_sinasc_para_CD.pdf``` (o nome do arquivo tal qual no portal do DataSUS).
# 
# ### Nosso objetivo
# Queremos deixar uma base organizada para podermos estudar a relação entre partos com risco para o bebê e algumas condições como tempo de parto, consultas de pré-natal etc.
# 
# #### Preparação da base
# 1. Carregue a base 'SINASC_RO_2019.csv'. Conte o número de registros e o número de registros não duplicados da base. Dica: você aprendeu um método que remove duplicados, encadeie este método com um outro método que conta o número de linhas. **Há linhas duplicadas?**  
# 
# 2. Conte o número de valores *missing* por variável.  
# 
# 3. Ok, no item anterior você deve ter achado pouco prático ler a informação de tantas variáveis, muitas delas nem devem ser interesantes. Então crie uma seleção dessa base somente com as colunas que interessam. São elas:
# ``` 
# ['LOCNASC', 'IDADEMAE', 'ESTCIVMAE', 'ESCMAE', 'QTDFILVIVO', 
#     'GESTACAO', 'GRAVIDEZ', 'CONSULTAS', 'APGAR5'] 
# ```
# Refaça a contagem de valores *missings*.  
# 
# 4. Apgar é uma *nota* que o pediatra dá ao bebê quando nasce de acordo com algumas características associadas principalmente à respiração. Apgar 1 e Apgar 5 são as notas 1 e 5 minutos do nascimento. Apgar5 será a nossa variável de interesse principal. Então remova todos os registros com Apgar5 não preenchido. Para esta seleção, conte novamente o número de linhas e o número de *missings*.  
# 
# 5. observe que as variáveis ```['ESTCIVMAE', 'CONSULTAS']``` possuem o código ```9```, que significa *ignorado*. Vamos assumir que o não preenchido é o mesmo que o código ```9```.<br>
# 6. Substitua os valores faltantes da quantitativa (```QTDFILVIVO```) por zero.  
# 7. Das restantes, decida que valore te parece mais adequado (um 'não preenchido' ou um valor 'mais provável' como no item anterior) e preencha. Justifique. Lembre-se de que tratamento de dados é trabalho do cientista, e que estamos tomando decisões a todo o momento - não há necessariamente certo e errado aqui.  
# 8. O Apgar possui uma classificação indicando se o bebê passou por asfixia:
# - Entre 8 e 10 está em uma faixa 'normal'. 
# - Entre 6 e 7, significa que o recém-nascido passou por 'asfixia leve'. 
# - Entre 4 e 5 significa 'asfixia moderada'.
# - Entre 0 e 3 significa 'asfixia severa'.  
# 
# Crie uma categorização dessa variável com essa codificação e calcule as frequências dessa categorização.  
# <br>
# 9. Renomeie as variáveis para que fiquem no *snake case*, ou seja, em letras minúsculas, com um *underscore* entre as palávras. Dica: repare que se você não quiser criar um *dataframe* novo, você vai precisar usar a opção ```inplace = True```.

# In[1]:


import pandas as pd
import requests

# 1) 
sinasc = pd.read_csv('SINASC_RO_2019.csv')
print(sinasc.shape)
sinasc.drop_duplicates().shape
# Não há duplicados
sinasc


# In[2]:


# 2) Contando dados faltantes
sinasc.isna().sum()


# In[3]:


# 3) Filtrando variáveis de interesse
base = pd.DataFrame(sinasc.loc[:,['LOCNASC', 'IDADEMAE', 'ESTCIVMAE', 'ESCMAE', 'QTDFILVIVO', 
 'GESTACAO', 'GRAVIDEZ', 'CONSULTAS', 'APGAR5']])
base.isna().sum()


# In[4]:


# 4) Limpando principal variável de interesse
base.dropna(subset=['APGAR5'],inplace=True)
print(base.isna().sum())
base


# In[5]:


# 5) Preenchendo as variáveis 'ESTCIVMAE' e 'CONSULTAS', dos dados faltantes para o valor 9(ignorado).
base['ESTCIVMAE'].fillna(9,inplace=True)
base['CONSULTAS'].fillna(9,inplace=True)
base.isna().sum()


# In[6]:


# 6) Preenchendo os dados faltantes da variável quantitativa 'QTDFILVIVO' para zero.
base['QTDFILVIVO'].fillna(0,inplace=True)
base.isna().sum()


# In[7]:


base.dtypes


# In[8]:


# 7) Preenchendo os dados faltantes das variáveis restantes

base['ESCMAE'].fillna('Ignorado',inplace=True)  # De acordo com o dicionário do SINASC a variável categórica 'ESCMAE' são os anos de escola da mãe, de acordo com pesquisas a maioria esmagadora das pessoas em RO foram pelo menos 1 ano de escola, e foram apenas 310 então conclui-se que seja um dado ignorado. 

base['GESTACAO'].fillna('Ignorado',inplace=True) # De acordo com o dicionário do SINASC a variável categórica 'GESTACAO' são as semanas da gestação que a paciente já passou, como o parto foi realizado presume-se que tenha uma categoria e foi ignorado, com isso conclui-se que foi dado ignorado.

base['GRAVIDEZ'].fillna('Ignorado',inplace=True) # De acordo com o dicionário do Sinasc a variável 'GRAVIDEZ' se resume ao tipo e quantidade de fetos, como o número de dados faltantes é baixo e a possibilidade de falsa gravidez mínima, conclui-se em dados ignorados.

base.isna().sum()


# In[ ]:





# In[9]:


# 8) Categorização da variável de interesse 'APGAR5'

base.loc[base['APGAR5']<=3,'respiracao'] = 'asfixia severa'
base.loc[(base['APGAR5']>3) & (base['APGAR5']<=5),'respiracao'] = 'Asfixia Moderada'
base.loc[(base['APGAR5']>5) & (base['APGAR5']<=7),'respiracao'] = 'Asfixia Leve'
base.loc[base['APGAR5']>=8,'respiracao'] = 'Normal'
base


# In[10]:


# 9) Renomeando as variáveis de interesse ao estilo snakecase

base.columns=['loc_nasc','idade_mae','est_civ_mae','esc_mae','qtd_fil_vivo','gestacao','gravidez','consultas','apgar_5','respiracao']
base

