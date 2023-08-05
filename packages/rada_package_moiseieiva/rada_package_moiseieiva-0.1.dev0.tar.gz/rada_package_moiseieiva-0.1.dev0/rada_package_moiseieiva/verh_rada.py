from rada_package_moiseieiva.rada_factories import UkraineRadaFactory, PolandRadaFactory

simulation_config_file = {'rada': 'Ukraine'}

def main():
    if simulation_config_file['rada'] == 'Ukraine':
        UkraineRadaFactory()().run()
    else:
        PolandRadaFactory()().run()


if __name__=="__main__":
    main()