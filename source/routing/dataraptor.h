#pragma once
#include "raptor_utils.h"
#include "type/pt_data.h"
namespace navitia { namespace routing { namespace raptor {

struct dataRAPTOR {

    //Données statiques
    const static uint32_t SECONDS_PER_DAY = 86400;
    std::vector<navitia::type::Connection> foot_path_forward;
    std::vector<pair_int> footpath_index_forward;
    std::vector<navitia::type::Connection> foot_path_backward;
    std::vector<pair_int> footpath_index_backward;
    std::multimap<navitia::type::idx_t, navitia::type::RoutePointConnection> footpath_rp_forward;
    std::multimap<navitia::type::idx_t, navitia::type::RoutePointConnection> footpath_rp_backward;
    std::vector<uint32_t> arrival_times;
    std::vector<uint32_t> departure_times;
    std::vector<uint32_t> start_times_frequencies;
    std::vector<uint32_t> end_times_frequencies;
    std::vector<std::bitset<366>> validity_patterns;
    std::vector<type::idx_t> st_idx_forward;
    std::vector<type::idx_t> st_idx_backward;
    std::vector<type::idx_t> vp_idx_forward;
    std::vector<type::idx_t> vp_idx_backward;
    std::vector<size_t> first_stop_time;
    std::vector<size_t> nb_trips;
    std::vector<size_t> first_frequency;
    std::vector<size_t> nb_frequencies;
    map_int_pint_t retour_constant;
    map_int_pint_t retour_constant_reverse;

    dataRAPTOR()  {}
    void load(const navitia::type::PT_Data &data);


    inline int get_stop_time_order(const type::Route & route, int orderVj, int order) const{
        return first_stop_time[route.idx] + (order * nb_trips[route.idx]) + orderVj;
    }
    inline uint32_t get_arrival_time(const type::Route & route, int orderVj, int order) const{
        if(orderVj < 0)
            return std::numeric_limits<uint32_t>::max();
        else
            return arrival_times[get_stop_time_order(route, orderVj, order)];
    }
    inline uint32_t get_departure_time(const type::Route & route, int orderVj, int order) const{
        if(orderVj < 0)
            return std::numeric_limits<uint32_t>::max();
        else
            return departure_times[get_stop_time_order(route, orderVj, order)];
    }
};

}}}

