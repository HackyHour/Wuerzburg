subroutine f(u, r)
implicit none
  real(kind(0.d0)), intent(out) :: r
  real(kind(0.d0)), intent(in) :: u
  r = u*(1.d0-u)
end subroutine f

subroutine  fortran_logistic(N, dt, u)
  integer, intent(in) :: N
  real(kind(0.d0)), intent(in) :: dt
  real(kind(0.d0)), intent(out) :: u(N)
  
  integer :: i
  real(kind(0.d0)) :: temp
  
  u(1) = 1.d-5
  do i=1, N-1
    call f(u(i), temp)
    u(i+1) = u(i) + dt*temp
  end do
end subroutine  fortran_logistic

program main

real(kind(0.d0)) :: start, finish, u(1000), dt
integer :: i, N

N = 1000
dt = 25.d0/1000.d0

call cpu_time(start)

do i = 1, 100000
  call fortran_logistic(N, dt, u)
end do

call cpu_time(finish)
print '(f6.3)', (finish-start)*1000000/100000
print *, u(1000)
end program
