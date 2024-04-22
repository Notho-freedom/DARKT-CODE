import subprocess

def new_cmd_commande(directorie: str, commande: str):
    try:
        result = subprocess.run(commande, shell=True, capture_output=True, text=True, cwd=directorie)

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return result.stderr.strip()
    except Exception as e:
        return str(e)

# directorie = input("Entrez le chemin du répertoire où exécuter la commande : ")
# commande = input("Entrez la commande à exécuter : ")
# resultat = new_cmd_commande(directorie, commande)
# print("Résultat de la commande :")
# print(resultat)
