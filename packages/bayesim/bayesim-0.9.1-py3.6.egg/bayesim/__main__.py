import argparse
import param_list as pml
import model as bym

def main(args=None):

 parser = argparse.ArgumentParser()


    # required values / analysis actions
    parser.add_argument('-o', '-output_variable', help='output variable')
    parser.add_argument('-obs', '-attach_observation', help='attach observation')
    parser.add_argument('-ec_x', 'ec_x_var', help='x-axis variable for data plot')
    parser.add_argument('-mod', '-attach_model', help='attach model')
    parser.add_argument('-run', help='run analysis', action='store_true')
    parser.add_argument('-sub', '-subdivide', help='subdivide', action='store_true')

    # optional stuff / tweaking behavior
    parser.add_argument('-name', '-state_name', help='state name')
    parser.add_argument('-save_step', help='Steps between two consecutive saved probabilities ')
    parser.add_argument('-th_pm', help='threshold in the probability mass')
    parser.add_argument('-th_pv', help='threshold in parameter space volume')
    parser.add_argument('-prb', '-plot_probability', help='plot probability', action='store_true')


    args = parser.parse_args()

    state_name =  vars(args).setdefault('state_name','bayesim_state.h5')

    # define output variable (eventually allow multiple)
    if 'o' in vars(args).keys() :
        m=bym.model(args.o)
        m.save_state() #State: only output

    # attach observed data
    if 'obs' in vars(args).keys() :
        m=bym.model(load_state=True, state_name=state_name)
        m.attach_observations(args.obs)
        m.save_state()

    # attach modeled data
    if 'mod' in vars(args).keys() :
        m=bym.model(load_state=True, state_name=state_name)
        m.attach_model(args.mod)
        m.save_state()

    # run inference
    if args.run:
        m=bym.model(load_state=True, state_name=state_name)
        m.run(vars(args)) # I think vars(args) should get th_pm and th_pv
        m.save_state()

    # subdivide the grid
    if args.subdivide:
        m=bym.model(load_state=True, state_name=state_name)
        m.subdivide(vars(args))
        m.save_state()

    # plot probabilities
    if args.prb:
        m=bym.model(load_state=True, state_name=state_name)
        m.visualize_probs(save_file=True)


    if ('th_pv' in vars(args).keys() or 'th_pm' in vars(args).keys()) and not args.subdivide:
    print('th_pv and/or th_pm are ignored unless -subdivide is passed')


if __name__ == "__main__":

    main()
