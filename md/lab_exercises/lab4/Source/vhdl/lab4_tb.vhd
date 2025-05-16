library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity lab4_tb is
end lab4_tb;

architecture Behavioral of lab4_tb is

    constant SYSCLK_PERIOD : time := 8 ns; -- 125MHz
    signal sysclk: std_logic := '0'; -- init to 0 for simulation
    signal reset_button : std_logic := '1';
    signal btn_pressed : std_logic := '1';
    signal rgb_led_5 : std_logic_vector(0 to 2) := "001";

    component lab4_top is
    port ( sysclk : in std_logic;
           btn : in std_logic_vector(1 downto 0);
           led5_r :  out std_logic;
           led5_g : out std_logic;
           led5_b : out std_logic
    );
    end component lab4_top;

begin

    -- Clock driver
    sysclk <= not sysclk after (SYSCLK_PERIOD / 2.0);

    stimulus_p: process
    begin
        -- after 10 clock cycles deassert reset
        wait for ( SYSCLK_PERIOD * 10 );
        reset_button <= '0';
                                       
        wait for (SYSCLK_PERIOD * 400);
        btn_pressed <= '0';
        
        wait for (SYSCLK_PERIOD * 200);
        btn_pressed <= '1';

        wait; -- wait here forever
    
    end process;
        
    -- Then, instantiate the DUT (Design Under Test)
    i_DUT: lab4_top
        port map (
            sysclk => sysclk,
            btn(0) => reset_button,
            btn(1) => btn_pressed,
            led5_r => rgb_led_5(2),
            led5_g => rgb_led_5(1),
            led5_b => rgb_led_5(0)
        );
end Behavioral;
