class Generator:
    pass

def spherical(
    pattern: dict = Pattern.get_pattern_from_toml(DEFAULT_PATH+'/pattern_benchmark.toml')
    ) -> list:
        """
        :param pattern: dict | dictionary with settings for generator
        :returns list | data to write to csv table
        """
        objects_data = []
        object_type = "dynamic"
        for i in range(0, pattern["number_of_objects"]):
            st_der = pattern["crit_mass_delta"] / 3
            position = Array.new_mx_from_list(pattern["center_pos"]) + Array.randarr_fixed_length(pattern["medium_radius"])
            velocity = Array.new_mx_from_list(pattern["center_mass_vel"]) + Array.randarr_fixed_length(pattern["medium_velocity_scalar"])
            objects_data.append(
                [
                    str(i),
                    str(object_type),
                    random.normal(pattern["medium_mass"], st_der),
                    position,
                    velocity,
                    Array.randarr_less_than_lenght(1, 3).m
                ])
        # print(*objects_data, sep="\n")
        return objects_data
