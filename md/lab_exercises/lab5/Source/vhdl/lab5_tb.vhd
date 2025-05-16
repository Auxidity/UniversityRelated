library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity lab5_tb is
end lab5_tb;

architecture Behavioral of lab5_tb is

    constant SYSCLK_PERIOD : time := 8 ns; -- 125MHz
    signal sysclk: std_logic := '0'; -- init to 0 for simulation
    signal reset_btn : std_logic := '1';
    signal select_channel_btn : std_logic := '1';
    signal increase_intensity_btn : std_logic := '0';
    signal decrease_intensity_btn : std_logic := '0';
    signal led4_r : std_logic := '0';
    signal led4_g : std_logic := '0';
    signal led4_b : std_logic := '0';
    signal rgb_led_5 : std_logic_vector(0 to 2) := "001";

    component lab5_top is
    port ( sysclk : in std_logic;
           btn : in std_logic_vector(3 downto 0);
           led4_r :  out std_logic;
           led4_g : out std_logic;
           led4_b : out std_logic;
           led5_r : out std_logic;
           led5_g : out std_logic;
           led5_b : out std_logic
    );
    end component lab5_top;

begin

    -- Clock driver
    sysclk <= not sysclk after (SYSCLK_PERIOD / 2.0);

    stimulus_p: process
    begin
        -- after 10 clock cycles deassert reset
        wait for ( SYSCLK_PERIOD * 10 );
        reset_btn <= '0';
                                       
        wait for (SYSCLK_PERIOD * 400);
        select_channel_btn <= '0';
        
        wait for (SYSCLK_PERIOD * 200);
        increase_intensity_btn <= '1';
        
        wait; -- wait here forever
    
    end process;
        
    -- Then, instantiate the DUT (Design Under Test)
    i_DUT: lab5_top
        port map (
            sysclk => sysclk,
            btn(0) => reset_btn,
            btn(1) => select_channel_btn,
            btn(2) => decrease_intensity_btn,
            btn(3) => increase_intensity_btn,
            led4_r => led4_r,
            led4_g => led4_g,
            led4_b => led4_b,
            led5_r => rgb_led_5(2),
            led5_g => rgb_led_5(1),
            led5_b => rgb_led_5(0)
        );
end Behavioral;
